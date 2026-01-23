Title: scripts/state_guard.sh — Instance safety guard for automation

Overview
The guard prevents wasting time or causing side effects on a fully-solved Juice Shop instance. It queries /api/Challenges, prints concise stats and any remaining unsolved keys, and exits non-zero when everything is already solved (unless you override with FORCE=1). Designed to be invoked at the top of automation scripts.

Key properties
- BASE: Defaults to http://127.0.0.1:3000
- Exit codes:
  - 0 → Proceed (instance not fully solved) or FORCE=1 set
  - 2 → HTTP/JSON error while reading /api/Challenges
  - 3 → Fully solved instance detected (override with FORCE=1)
- Counts both hacking and coding challenges using ground-truth /api/Challenges.
- Prints a newline-separated list of unsolved challenge keys for easy grepping/targeting.

Usage
- Default base:
  ./scripts/state_guard.sh

- Custom base:
  BASE=http://127.0.0.1:3000 ./scripts/state_guard.sh

- Override when you intentionally want to run anyway:
  FORCE=1 ./scripts/state_guard.sh

Recommended integration (bash)
Place this near the top of your scripts:

scripts/state_guard.sh || {
  code=$?
  if [ "$code" -eq 3 ]; then
    echo "Instance is fully solved. Aborting (override with FORCE=1)." >&2
    exit 0
  else
    exit "$code"
  fi
}

Notes and tips
- Always prefer 127.0.0.1 over localhost to avoid cookie/origin mismatches.
- Cookie vs Bearer does not matter for /api/Challenges (it’s public), but many other endpoints do care. Keep the distinction sharp in your automation.
- This guard is intentionally lightweight; it does not cache anything and has minimal dependencies (curl + Python).
