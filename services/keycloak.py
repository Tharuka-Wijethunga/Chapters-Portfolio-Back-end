from typing import List, Optional

import httpx
from fastapi import HTTPException

from core.config import settings
from schemas.keycloak import KeycloakUser

DEFAULT_TIMEOUT = 10.0


def _handle_httpx_error(exc: httpx.HTTPError) -> None:
    raise HTTPException(status_code=502, detail=f"Error communicating with Keycloak: {exc}")


def get_keycloak_token() -> Optional[str]:
    try:
        resp = httpx.post(
            f"{settings.KEYCLOAK_URL}/realms/{settings.REALM}/protocol/openid-connect/token",
            data={
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
                "grant_type": "client_credentials",
            },
            timeout=DEFAULT_TIMEOUT,
        )
    except httpx.HTTPError as exc:
        _handle_httpx_error(exc)
    if resp.status_code == 200:
        return resp.json().get("access_token")
    if resp.status_code == 401:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized access - invalid client or credentials for Keycloak",
        )
    raise HTTPException(
        status_code=resp.status_code,
        detail=f"Failed to retrieve Keycloak token: {resp.text}",
    )


def get_all_users() -> List[KeycloakUser]:
    token = get_keycloak_token()
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized access - empty token received from Keycloak",
        )
    try:
        resp = httpx.get(
            f"{settings.KEYCLOAK_URL}/admin/realms/{settings.REALM}/users",
            headers={"Authorization": f"Bearer {token}"},
            timeout=DEFAULT_TIMEOUT,
        )
    except httpx.HTTPError as exc:
        _handle_httpx_error(exc)
    if resp.status_code == 200:
        return [KeycloakUser(**user) for user in resp.json()]
    raise HTTPException(
        status_code=resp.status_code,
        detail=f"Keycloak returned a {resp.status_code} - {resp.text} error",
    )


def get_user_by_id(user_id: str) -> KeycloakUser:
    token = get_keycloak_token()
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized access - empty token received from Keycloak",
        )
    try:
        resp = httpx.get(
            f"{settings.KEYCLOAK_URL}/admin/realms/{settings.REALM}/users/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=DEFAULT_TIMEOUT,
        )
    except httpx.HTTPError as exc:
        _handle_httpx_error(exc)
    if resp.status_code == 200:
        return KeycloakUser(**resp.json())
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail=f"User not found with ID: {user_id}")
    raise HTTPException(
        status_code=resp.status_code,
        detail=f"Keycloak returned a {resp.status_code} - {resp.text} error",
    )


def get_all_users_safely() -> list[KeycloakUser]:
    try:
        return get_all_users()
    except HTTPException as exc:
        print(f"\nError fetching users from keycloak:\n{exc}\n")
        return []


def get_user_by_id_safely(
    user_id: str,
    *,
    default_username: str = "",
    default_profile_pic_url: str = "",
) -> KeycloakUser:
    try:
        return get_user_by_id(user_id)
    except HTTPException as exc:
        print(f"\nError fetching user {user_id} from keycloak:\n{exc}\n")
        return KeycloakUser(username=default_username, profile_pic_url=default_profile_pic_url)
