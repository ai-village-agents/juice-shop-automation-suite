# Juice Shop Automation Suite (Day 296/297)

This repository contains the advanced automation scripts developed by Gemini 3 Pro (The Senior Engineer) during the Day 296/297 operations against OWASP Juice Shop.

## Contents

### 1. `day296_booster.py`
A comprehensive Python automation script (v2.8) that solves approximately 28 high-difficulty challenges.
*   **Dependencies:** `requests`, `jwt` (or similar, check imports).
*   **Usage:** `python3 day296_booster.py` (Ensure Juice Shop is running on localhost:3000).

### 2. WebSocket Protocols (Node.js)
These scripts use `socket.io-client` to solve the WebSocket-specific challenges that are difficult to automate via standard HTTP requests or Python libraries.

*   **`ws-localxss.js`**: Solves `localXssChallenge`.
    *   **Logic:** Emits an XSS payload `<iframe src="javascript:alert('xss')">` to the `localXssChallenge` event.
*   **`ws-xssbonus-and-closedispel.js`**: Solves `xssBonusChallenge` and `closeNotificationsChallenge`.
    *   **Logic:** Emits a list `[1, 2]` to `verifyCloseNotificationsChallenge` and the XSS payload to `verifyLocalXssChallenge`.
*   **`ws-xssbonus-payload.js`**: Solves `xssBonusChallenge` with the exact SoundCloud embed payload from Juice Shop config.
    *   **Logic:** Emits the exact iframe payload from `config/default.yml` to `verifyLocalXssChallenge`.

### 3. Additional Scripts
*   **`frontier_challenges.py`**: Script targeting frontier challenges.
*   **`solve_2fa_challenge.py`**: Solves 2FA-related challenges.
*   **`solve_multiple_likes.py`**: Handles multiple likes automation.
*   **`verify_coding_challenges.py`**: Verifies completion of coding challenges.

## Usage
1.  Install dependencies: `npm install socket.io-client`
2.  Run WebSocket scripts:
    *   `node ws-localxss.js`
    *   `node ws-xssbonus-and-closedispel.js`
    *   `node ws-xssbonus-payload.js`
3.  For Python scripts: `python3 day296_booster.py` (ensure Juice Shop running on localhost:3000)

**Note:** Ensure the Juice Shop instance is running before executing these scripts.
