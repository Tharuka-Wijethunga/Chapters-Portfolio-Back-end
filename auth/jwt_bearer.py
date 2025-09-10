from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decode_jwt
from config.config import settings

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, allowed_roles: list = None):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.allowed_roles = allowed_roles or []

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            
            payload = self.verify_jwt(credentials.credentials)
            
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")

            if self.allowed_roles:
                user_roles = self.get_user_roles(payload)
                print(f"User roles from token: {user_roles}")
                if not any(role in user_roles for role in self.allowed_roles):
                    raise HTTPException(status_code=403, detail="You don't have permission to access this resource.")
            
            return payload
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> dict:
        return decode_jwt(jwtoken)

    def get_user_roles(self, payload: dict) -> list:
        # Keycloak roles are checked in 'resource_access' for our specific client_id
        try:
            return payload.get("resource_access", {}).get(settings.CLIENT_ID, {}).get("roles", [])
        except AttributeError:
            return []