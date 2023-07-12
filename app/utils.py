import httpx
from .const import HUNTER_API_KEY

HUNTER_API_URL = "https://api.hunter.io/v2/email-verifier"

def verify_email(email: str) -> tuple[bool, str]:
    response = httpx.get(HUNTER_API_URL, params={"email": email, "api_key": HUNTER_API_KEY})
    
    if response.status_code == 202:
        return False, "Could not verify email. Try again later."
    if response.status_code == 451:
        return True, ""
    
    errors = {
        202: "Could not verify email. Try again later.",
        222: "Internal error. Try again later.",
        400: "Invalid request.",
        429: "Too many requests.",
        401: "API key is invalid or missing."
    }
    if response.status_code in errors:
        return False, errors[response.status_code]
    

    data = response.json()

    if data["data"]["status"] not in ["invalid", "unknown"]:
        return True, ""
    
    return False, "Email is not valid"