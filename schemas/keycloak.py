from pydantic import BaseModel

class KeycloakUser(BaseModel):
    username: str
    profile_pic_url: str = ""