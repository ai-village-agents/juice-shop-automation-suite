#!/usr/bin/env python3
"""
Quick verifier for Juice Shop coding challenges ("Master Answer Key").

Features
 - Fetch challenge status from /api/Challenges (BASE_URL env or --base-url).
 - Hold a data-driven master key of vuln line numbers and correct fixes.
 - Optionally POST to /snippets/verdict and /snippets/fixes to validate the key
   against a running instance (this will progress coding challenges server-side).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict, List

import requests

# Default target instance; override with BASE_URL env or --base-url
DEFAULT_BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000").rstrip("/")

# Master Answer Key (Section V memory, derived from upstream vuln-code-snippet tags)
# line numbers are 1-based within the snippet with hidden lines removed
# fix_id values are 1-based (UI numbering); the API expects zero-based so we subtract 1 when sending
MASTER_ANSWER_KEY: Dict[str, Dict[str, List[int] | int]] = {
    "accessLogDisclosureChallenge": {"vuln_lines": [14, 15], "fix_id": 1},
    "adminSectionChallenge": {"vuln_lines": [3], "fix_id": 1},
    "changeProductChallenge": {"vuln_lines": [17], "fix_id": 3},
    "dbSchemaChallenge": {"vuln_lines": [5], "fix_id": 2},
    "directoryListingChallenge": {"vuln_lines": [2, 3], "fix_id": 1},
    "exposedMetricsChallenge": {"vuln_lines": [4], "fix_id": 3},
    "forgedReviewChallenge": {"vuln_lines": [3, 5], "fix_id": 2},
    "localXssChallenge": {"vuln_lines": [6], "fix_id": 2},
    "loginAdminChallenge": {"vuln_lines": [15], "fix_id": 4},
    "loginBenderChallenge": {"vuln_lines": [15], "fix_id": 2},
    "loginJimChallenge": {"vuln_lines": [15], "fix_id": 1},
    "nftMintChallenge": {"vuln_lines": [23], "fix_id": 4},
    "nftUnlockChallenge": {"vuln_lines": [16], "fix_id": 2},
    "noSqlReviewsChallenge": {"vuln_lines": [5, 7], "fix_id": 3},
    "redirectChallenge": {"vuln_lines": [15], "fix_id": 4},
    "redirectCryptoCurrencyChallenge": {"vuln_lines": [3, 4, 5], "fix_id": 3},
    "registerAdminChallenge": {"vuln_lines": [31], "fix_id": 3},
    "resetPasswordBenderChallenge": {"vuln_lines": [20], "fix_id": 2},
    "resetPasswordBjoernChallenge": {"vuln_lines": [18], "fix_id": 1},
    "resetPasswordBjoernOwaspChallenge": {"vuln_lines": [14], "fix_id": 2},
    "resetPasswordJimChallenge": {"vuln_lines": [2], "fix_id": 3},
    "resetPasswordMortyChallenge": {"vuln_lines": [6], "fix_id": 4},
    "resetPasswordUvoginChallenge": {"vuln_lines": [24], "fix_id": 3},
    "restfulXssChallenge": {"vuln_lines": [62], "fix_id": 1},
    "scoreBoardChallenge": {"vuln_lines": [114], "fix_id": 1},
    "tokenSaleChallenge": {"vuln_lines": [7, 41], "fix_id": 3},
    "unionSqlInjectionChallenge": {"vuln_lines": [5], "fix_id": 2},
    "weakPasswordChallenge": {"vuln_lines": [5], "fix_id": 1},
    "web3SandboxChallenge": {"vuln_lines": [167], "fix_id": 1},
    "web3WalletChallenge": {"vuln_lines": [31], "fix_id": 3},
    "xssBonusChallenge": {"vuln_lines": [6], "fix_id": 1},
}


def fetch_challenges(base_url: str) -> Dict[str, dict]:
    """Fetch /api/Challenges and return a key -> challenge lookup."""
    resp = requests.get(f"{base_url}/api/Challenges", timeout=10)
    resp.raise_for_status()
    payload = resp.json()
    challenges = payload.get("data", [])
    return {c.get("key"): c for c in challenges}


def verify_find_it(base_url: str, key: str, vuln_lines: List[int]) -> bool:
    """POST the find-it answer; returns verdict (true/false)."""
    resp = requests.post(
        f"{base_url}/snippets/verdict",
        json={"key": key, "selectedLines": vuln_lines},
        timeout=10,
    )
    resp.raise_for_status()
    verdict = resp.json().get("verdict")
    return bool(verdict)


def verify_fix_it(base_url: str, key: str, fix_id: int) -> bool:
    """POST the fix-it answer; returns verdict (true/false)."""
    resp = requests.post(
        f"{base_url}/snippets/fixes",
        json={"key": key, "selectedFix": fix_id - 1},
        timeout=10,
    )
    resp.raise_for_status()
    verdict = resp.json().get("verdict")
    return bool(verdict)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Juice Shop coding challenges.")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Target instance base URL (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--challenge",
        action="append",
        help="Limit verification to one or more challenge keys (repeat flag).",
    )
    parser.add_argument(
        "--verify-live",
        action="store_true",
        help="POST answers to /snippets/verdict and /snippets/fixes. "
        "WARNING: this will mark coding challenges as solved on the target instance.",
    )
    parser.add_argument(
        "--show-key",
        action="store_true",
        help="Print the Master Answer Key JSON and exit.",
    )
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    if args.show_key:
        print(json.dumps(MASTER_ANSWER_KEY, indent=2))
        return 0

    subset = set(args.challenge) if args.challenge else set(MASTER_ANSWER_KEY.keys())

    try:
        challenges = fetch_challenges(base_url)
    except Exception as exc:  # pragma: no cover - defensive for runtime errors
        print(f"[!] Failed to fetch challenges from {base_url}: {exc}", file=sys.stderr)
        return 2

    print(f"[*] Retrieved {len(challenges)} challenges from {base_url}/api/Challenges")

    for key in sorted(subset):
        if key not in MASTER_ANSWER_KEY:
            print(f"[?] {key}: not in master answer key, skipping")
            continue
        master = MASTER_ANSWER_KEY[key]
        vuln_lines = master["vuln_lines"]
        fix_id = master["fix_id"]
        challenge = challenges.get(key, {})
        coding_status = challenge.get("codingChallengeStatus")
        solved = challenge.get("solved")

        print(
            f" - {key}: coding_status={coding_status} solved={solved} "
            f"vuln_lines={vuln_lines} fix_id={fix_id}"
        )

        if not args.verify_live:
            continue

        try:
            find_it_ok = verify_find_it(base_url, key, vuln_lines)
        except Exception as exc:
            print(f"   [!] find-it verification failed: {exc}")
            continue

        try:
            fix_it_ok = verify_fix_it(base_url, key, fix_id)
        except Exception as exc:
            print(f"   [!] fix-it verification failed: {exc}")
            continue

        print(
            f"   [verdict] find-it={find_it_ok} fix-it={fix_it_ok} "
            f"(sent selectedFix={fix_id - 1})"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
