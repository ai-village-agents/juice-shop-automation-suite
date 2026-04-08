#!/usr/bin/env python3
"""Solve OWASP Juice Shop 'Coding Challenges' via the public snippets API.

This script is intentionally conservative:
- It checks /api/Challenges first and refuses to run on fully-solved instances
  unless --force or FORCE=1.
- It exits non-zero on any failure by default.

For training/local Juice Shop instances only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Tuple


# challengeKey -> (vulnLines (1-based), fixIndex (0-based))
CODING_MAP: Dict[str, Tuple[List[int], int]] = {
    "accessLogDisclosureChallenge": ([14, 15], 0),
    "adminSectionChallenge": ([3], 0),
    "changeProductChallenge": ([17], 2),
    "dbSchemaChallenge": ([5], 1),
    "directoryListingChallenge": ([2, 3], 0),
    "exposedMetricsChallenge": ([4], 2),
    "forgedReviewChallenge": ([3, 5], 1),
    "localXssChallenge": ([6], 1),
    "loginAdminChallenge": ([15], 3),
    "loginBenderChallenge": ([15], 1),
    "loginJimChallenge": ([15], 0),
    "nftMintChallenge": ([23], 3),
    "nftUnlockChallenge": ([16], 1),
    "noSqlReviewsChallenge": ([5, 7], 2),
    "redirectChallenge": ([15], 3),
    "redirectCryptoCurrencyChallenge": ([3, 4, 5], 2),
    "registerAdminChallenge": ([31], 2),
    "resetPasswordBenderChallenge": ([20], 1),
    "resetPasswordBjoernChallenge": ([18], 0),
    "resetPasswordBjoernOwaspChallenge": ([14], 1),
    "resetPasswordJimChallenge": ([2], 2),
    "resetPasswordMortyChallenge": ([6], 3),
    "resetPasswordUvoginChallenge": ([24], 2),
    "restfulXssChallenge": ([62], 0),
    "scoreBoardChallenge": ([114], 0),
    "tokenSaleChallenge": ([7, 41], 2),
    "unionSqlInjectionChallenge": ([5], 1),
    "weakPasswordChallenge": ([5], 0),
    "web3SandboxChallenge": ([167], 0),
    "web3WalletChallenge": ([31], 2),
    "xssBonusChallenge": ([6], 0),
}


def _json_req(method: str, url: str, payload: Any | None, timeout: float = 30.0) -> Any:
    """Send a JSON HTTP request and return decoded JSON or raise with context."""
    data = None
    headers = {
        "Accept": "application/json",
        "User-Agent": "ai-village-js-quickwins/solve_coding_challenges",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, method=method, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
    except urllib.error.HTTPError as e:
        body = e.read() if hasattr(e, "read") else b""
        raise RuntimeError(f"HTTP {e.code} {method} {url}: {body[:200]!r}") from e
    except Exception as e:
        raise RuntimeError(f"Request failed: {method} {url}: {e}") from e

    try:
        return json.loads(body.decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"Non-JSON response from {method} {url}: {body[:200]!r}") from e


def get_challenges(base: str) -> List[Dict[str, Any]]:
    """Fetch and return the challenges list from a Juice Shop instance."""
    j = _json_req("GET", f"{base}/api/Challenges", None)
    data = j.get("data", j)
    if not isinstance(data, list):
        raise RuntimeError("Unexpected /api/Challenges JSON shape")
    return data


def guard_not_fully_solved(base: str, force: bool) -> Tuple[int, int, List[Dict[str, Any]]]:
    """Abort on fully solved instances unless overridden; return counts and data."""
    ch = get_challenges(base)
    total = len(ch)
    solved = sum(1 for c in ch if c.get("solved"))
    if total and solved == total and not force:
        raise SystemExit(
            f"Phantom wipe suspected: /api/Challenges reports {solved}/{total} solved. "
            "Refusing to run (use --force or FORCE=1 to override)."
        )
    return solved, total, ch


def solve_one(base: str, key: str, lines: List[int], fix_idx: int, dry_run: bool) -> None:
    """Submit verdict and fix for a single coding challenge key."""
    if dry_run:
        print(f"[dry-run] {key}: verdict lines={lines} then apply fix index={fix_idx}")
        return

    verdict = _json_req(
        "POST",
        f"{base}/snippets/verdict",
        {"key": key, "selectedLines": lines},
    )
    if not isinstance(verdict, dict) or verdict.get("verdict") is not True:
        raise RuntimeError(f"verdict failed for {key}: {verdict}")

    fix = _json_req(
        "POST",
        f"{base}/snippets/fixes",
        {"key": key, "selectedFix": fix_idx},
    )
    if not isinstance(fix, dict) or fix.get("verdict") is not True:
        raise RuntimeError(f"fix failed for {key}: {fix}")


def parse_only(s: str) -> List[str]:
    """Parse a comma-separated list of challenge keys into a cleaned list."""
    keys = [k.strip() for k in s.split(",") if k.strip()]
    return keys


def main(argv: List[str]) -> int:
    """Entry point for solving Juice Shop coding challenges via the snippets API."""
    p = argparse.ArgumentParser(
        description="Solve all Juice Shop Coding Challenges using /snippets/* API",
    )
    p.add_argument(
        "--base",
        default=os.environ.get("BASE", "http://127.0.0.1:3000"),
        help="Base URL (default: BASE env or http://127.0.0.1:3000)",
    )
    p.add_argument("--dry-run", action="store_true", help="Print actions without sending requests")
    p.add_argument("--force", action="store_true", help="Override the fully-solved safety guard")
    p.add_argument(
        "--only",
        default="",
        help="Comma-separated subset of challenge keys to run (e.g. loginAdminChallenge,scoreBoardChallenge)",
    )
    p.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Keep going if one key fails; still exits non-zero if any failures occurred",
    )
    p.add_argument(
        "--unsolved-only",
        action="store_true",
        help="Skip coding keys already solved according to /api/Challenges",
    )
    args = p.parse_args(argv)

    base = args.base.rstrip("/")
    force = args.force or os.environ.get("FORCE") == "1"

    # Safety guard against running on already-solved instances.
    solved, total, challenges = guard_not_fully_solved(base, force=force)
    print(f"/api/Challenges: solved {solved}/{total}")

    keys = list(CODING_MAP.keys())
    if args.only:
        wanted = set(parse_only(args.only))
        unknown = sorted(wanted.difference(keys))
        if unknown:
            raise SystemExit(f"Unknown coding challenge keys in --only: {', '.join(unknown)}")
        keys = [k for k in keys if k in wanted]

    challenges_by_key = {c.get("key"): c for c in challenges if isinstance(c, dict)}
    if args.unsolved_only:
        before = len(keys)
        keys = [k for k in keys if not challenges_by_key.get(k, {}).get("solved")]
        skipped = before - len(keys)
        print(f"Skipping already-solved coding keys: {skipped}")

    print(f"Will process {len(keys)}/{len(CODING_MAP)} coding challenges")

    failures: List[str] = []
    for i, key in enumerate(keys, 1):
        lines, fix_idx = CODING_MAP[key]
        try:
            solve_one(base, key, lines, fix_idx, dry_run=args.dry_run)
            if not args.dry_run:
                print(f"[{i:02d}/{len(keys):02d}] OK  {key}")
            else:
                print(f"[{i:02d}/{len(keys):02d}] DRY {key}")
        except Exception as e:
            msg = f"[{i:02d}/{len(keys):02d}] FAIL {key}: {e}"
            print(msg, file=sys.stderr)
            failures.append(key)
            if not args.continue_on_error:
                break
        # gentle pacing to avoid hammering a fragile instance
        time.sleep(0.05)

    # Post-check: how many of the 31 are now solved?
    if not args.dry_run:
        ch = get_challenges(base)
        by_key = {c.get("key"): c for c in ch if isinstance(c, dict)}
        solved_now = sum(1 for k in CODING_MAP.keys() if by_key.get(k, {}).get("solved"))
        print(f"Coding challenges solved now: {solved_now}/{len(CODING_MAP)}")

    if failures:
        print(f"Failures: {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
