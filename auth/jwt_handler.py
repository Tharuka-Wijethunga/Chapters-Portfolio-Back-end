import requests
import time
from jose import jwt
from jose.exceptions import JOSEError
from core.config import settings

# A simple in-memory cache for JWKS to avoid fetching on every request
jwks_cache = {
    "keys": [],
    "expires_at": 0
}

def get_jwks():
    """
    Fetches the JSON Web Key Set (JWKS) from Keycloak.
    Keys are cached for 10 minutes.
    """
    global jwks_cache
    if time.time() < jwks_cache["expires_at"]:
        return jwks_cache["keys"]

    try:
        jwks_url = f"{settings.KEYCLOAK_URL}/realms/{settings.REALM}/protocol/openid-connect/certs"
        response = requests.get(jwks_url, timeout=10)
        response.raise_for_status()
        jwks = response.json()
        
        # Cache for 10 minutes
        jwks_cache["keys"] = jwks.get("keys", [])
        jwks_cache["expires_at"] = time.time() + 600
        
        return jwks_cache["keys"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JWKS from Keycloak: {e}")
        return []

def decode_jwt(token: str) -> dict:
    """
    Decodes and validates a JWT from Keycloak using its public key.
    """
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        
        jwks = get_jwks()
        if not jwks:
            return {}

        rsa_key = {}
        for key in jwks:
            if key["kid"] == kid:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
                break

        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=settings.CLIENT_ID,
                issuer=f"{settings.KEYCLOAK_URL}/realms/{settings.REALM}"
            )
            return payload
            
    except JOSEError as e:
        # This will catch expired signatures, invalid claims, etc.
        print(f"JWT decoding error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during JWT decoding: {e}")
        
    return {}