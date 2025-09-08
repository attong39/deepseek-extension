# Sending Signed Requests (HMAC) to ZETA API

This guide shows how to generate and send request signatures compatible with ZeroTrust middleware.

## Prerequisites

- Server has a shared secret configured
  - Environment or settings: `request_signature_secret = "<your-secret>"`
  - To enforce signatures for all requests: `require_request_signature = true`
- Default header name: `X-Request-Signature`
- Signature format: `sha256=<hex-digest>`
- Payload used for signature: raw HTTP request body bytes

## Python example

```python
import hashlib, hmac, requests
secret = b"your-shared-secret"
body = b'{"a": 1}'
digest = hmac.new(secret, body, hashlib.sha256).hexdigest()
headers = {"X-Request-Signature": f"sha256={digest}", "Content-Type": "application/json"}
r = requests.post("http://localhost:8000/api/v1/privacy/sanitize", data=body, headers=headers)
print(r.status_code, r.json())
```

## Node.js example

```js
const crypto = require("crypto");
const fetch = require("node-fetch");
const secret = Buffer.from("your-shared-secret", "utf8");
const body = Buffer.from('{"a": 1}', "utf8");
const h = crypto.createHmac("sha256", secret).update(body).digest("hex");
const headers = {
  "X-Request-Signature": `sha256=${h}`,
  "Content-Type": "application/json",
};
fetch("http://localhost:8000/api/v1/privacy/sanitize", { method: "POST", body, headers })
  .then(r => r.json())
  .then(console.log);
```

## curl example (Linux/macOS)

```bash
SECRET="your-shared-secret"
BODY='{"a": 1}'
SIG=$(printf "%s" "$BODY" | openssl dgst -sha256 -hmac "$SECRET" -r | awk '{print $1}')
curl -s -X POST \
  -H "X-Request-Signature: sha256=$SIG" \
  -H "Content-Type: application/json" \
  --data "$BODY" \
  <http://localhost:8000/api/v1/privacy/sanitize>
```

## Notes

- If `require_request_signature = true` and a request does not include a valid signature, the server returns 401.
- When `zero_trust_rate_limit_enabled = false`, throttling can be handled entirely by the dedicated rate-limiting middleware.
- Keep secrets out of source control; use environment variables or a secret manager.
