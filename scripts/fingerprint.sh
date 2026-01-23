#!/usr/bin/env bash
set -euo pipefail

# Fingerprint the local Juice Shop instance for stability checks and cross-agent comparisons.
# Outputs:
# - listener_3000=...               → listener line for :3000 or a status
# - solved_keys_count=N             → number of solved challenge keys (hacking or coding fix)
# - solved_keys_sha256=<hex>        → SHA256 over canonical JSON of sorted solved keys
# - rest_admin_appcfg_sha256=<hex|SKIPPED|UNAVAILABLE(HTTP_xxx)> → optional admin config hash when ADMIN_BEARER is provided
#
# Env:
# - BASE (default http://127.0.0.1:3000)
# - ADMIN_BEARER (optional; Bearer token with admin privileges)

BASE="${BASE:-http://127.0.0.1:3000}"
CH_TMP=$(mktemp)
ADM_TMP=$(mktemp)
cleanup() { rm -f "$CH_TMP" "$ADM_TMP" 2>/dev/null || true; }
trap cleanup EXIT

# 1) Listener
listener=""
if command -v ss >/dev/null 2>&1; then
  listener=$(ss -plnt 2>/dev/null | awk '$4 ~ /:3000$/ {print $0}') || true
fi
if [ -z "${listener}" ] && command -v netstat >/dev/null 2>&1; then
  listener=$(netstat -plnt 2>/dev/null | awk '$4 ~ /:3000$/ {print $0}') || true
fi
if [ -z "${listener}" ]; then
  listener="not_listening"
fi
printf 'listener_3000=%s\n' "${listener}"

# 2) Solved keys hash
http_code=$(curl -sS -w '%{http_code}' -o "$CH_TMP" "$BASE/api/Challenges" || true)
if [ "$http_code" != "200" ]; then
  echo "ERROR: Unable to reach $BASE/api/Challenges (HTTP $http_code)" >&2
  exit 2
fi
python3 - "$CH_TMP" <<'PY'
import sys, json, hashlib
p=sys.argv[1]
j=json.load(open(p,'r',encoding='utf-8'))
chs=j.get('data',[])
# A key is considered solved if hacking is solved OR its coding Fix-It is solved.
solved=[c.get('key') for c in chs if c.get('solved') or c.get('codingChallengeStatus')==2]
solved=[k for k in solved if k]
solved_sorted=sorted(set(solved))
canonical=json.dumps(solved_sorted, separators=(',',':'))
hashv=hashlib.sha256(canonical.encode()).hexdigest()
print(f"solved_keys_count={len(solved_sorted)}")
print(f"solved_keys_sha256={hashv}")
PY

# 3) Optional admin application configuration hash
if [ -n "${ADMIN_BEARER:-}" ]; then
  h=$(curl -sS -w '%{http_code}' -H "Authorization: Bearer ${ADMIN_BEARER}" -o "$ADM_TMP" "$BASE/rest/admin/application-configuration" || true)
  if [ "$h" = "200" ]; then
    python3 - "$ADM_TMP" <<'PY'
import sys, json, hashlib
j=json.load(open(sys.argv[1],'r',encoding='utf-8'))
canon=json.dumps(j, sort_keys=True, separators=(',',':'))
print("rest_admin_appcfg_sha256=" + hashlib.sha256(canon.encode()).hexdigest())
PY
  else
    echo "rest_admin_appcfg_sha256=UNAVAILABLE(HTTP_${h})"
  fi
else
  echo "rest_admin_appcfg_sha256=SKIPPED"
fi
