Title: scripts/fingerprint.sh — Deterministic instance fingerprint

What it does
Produces a compact, reproducible fingerprint of your Juice Shop instance:
- listener_3000: Whether a process is listening on :3000 (via ss/netstat)
- solved_keys_count: Count of solved challenge keys
- solved_keys_sha256: SHA256 over a canonical JSON array of all solved challenge keys (sorted, deduplicated)
- rest_admin_appcfg_sha256: Optional hash of /rest/admin/application-configuration (requires ADMIN_BEARER)

Why this matters
Multiple independent instances are in play. A short, deterministic fingerprint helps verify whether you’re targeting the same instance across sessions and whether your local state matches teammates’ reports.

Definition of “solved keys”
A challenge key is included if either:
- hacking challenge is solved (challenge.solved == true), or
- its coding “Fix-It” is solved (codingChallengeStatus == 2).
The script queries the single source of truth: GET /api/Challenges.

Usage
- Basic:
  ./scripts/fingerprint.sh

- Explicit base:
  BASE=http://127.0.0.1:3000 ./scripts/fingerprint.sh

- Include admin configuration hash:
  ADMIN_BEARER=eyJ... ./scripts/fingerprint.sh

Outputs (example)
listener_3000: tcp LISTEN 0 511 127.0.0.1:3000 users:("node",pid=1234,fd=23)
solved_keys_count=74
solved_keys_sha256=1f5b0c2e0e1b...d97
rest_admin_appcfg_sha256=0a7f3b6b3c...411

Notes
- Prefer 127.0.0.1 over localhost to avoid cookie/origin mismatches.
- Only curl and Python are required. If neither ss nor netstat exist, listener_3000 prints "not_listening".
- The admin config hash is optional and primarily useful for deep state comparisons.
