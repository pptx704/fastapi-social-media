import httpx
from .const import HUNTER_API_KEY

HUNTER_API_URL = "https://api.hunter.io/v2/email-verifier"

def verify_email(email: str):
    response = httpx.get(HUNTER_API_URL, params={"email": email, "api_key": HUNTER_API_KEY})
    if response.status_code != 200:
        return False

    data = response.json()

    return data["data"]["status"] != "invalid"