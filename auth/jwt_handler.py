import time
from typing import Dict

import jwt
from config.config import Settings

secret_key = Settings().secret_key


def token_response(token: str):
    return {"access_token": token}


def sign_jwt(user_id: str, role: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "role": role,
        "expires": time.time() + Settings().expires_in
    }
    return token_response(jwt.encode(payload, secret_key, algorithm="HS256"))


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    return decoded_token if decoded_token["expires"] >= time.time() else {}
