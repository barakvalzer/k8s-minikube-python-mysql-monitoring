import os
import base64
import requests
import secrets
import string
from nacl import encoding, public

# CONFIGURE THIS
REPO = "barakvalzer/k8s-minikube-python-mysql-monitoring"
TOKEN = os.environ["GH_PAT"]  # GitHub PAT as environment variable
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}

# 1. Get repo's public key for secrets
r = requests.get(f"https://api.github.com/repos/{REPO}/actions/secrets/public-key", headers=HEADERS)
r.raise_for_status()
data = r.json()
key_id = data["key_id"]
key = data["key"]

# 2. Encrypt the secret using LibSodium
def encrypt(public_key: str, secret_value: str) -> str:
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

# 3. Generate random user and password
username = "user-" + ''.join(secrets.choice(string.ascii_lowercase) for _ in range(5))
password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))

# 4. Upload to GitHub secrets
def upload_secret(name, value):
    encrypted = encrypt(key, value)
    url = f"https://api.github.com/repos/{REPO}/actions/secrets/{name}"
    payload = {"encrypted_value": encrypted, "key_id": key_id}
    r = requests.put(url, headers=HEADERS, json=payload)
    r.raise_for_status()

upload_secret("ARGOCD_USERNAME", username)
upload_secret("ARGOCD_PASSWORD", password)

print("✅ GitHub secrets set:")
print(f"- ARGOCD_USERNAME = {username}")
print(f"- ARGOCD_PASSWORD = {password}")