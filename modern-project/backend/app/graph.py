from datetime import datetime, timedelta
from typing import Dict

import httpx
import msal
from sqlmodel import Session

from .config import get_settings
from .models import TenantConfig

settings = get_settings()


class GraphClient:
    def __init__(self, session: Session):
        self.session = session
        self._token_cache: Dict[str, Dict[str, str]] = {}

    def _get_authority(self, tenant: TenantConfig) -> str:
        return f"{tenant.authority_host}/{tenant.tenant_id}"

    def _acquire_token(self, tenant: TenantConfig) -> str:
        cached = self._token_cache.get(tenant.tenant_id)
        if cached and cached["expires_at"] > datetime.utcnow():
            return cached["token"]

        app = msal.ConfidentialClientApplication(
            tenant.client_id,
            authority=self._get_authority(tenant),
            client_credential=tenant.client_secret,
        )
        result = app.acquire_token_for_client(scopes=tenant.scopes or [settings.graph_scope])
        token = result.get("access_token")
        if token is None:
            raise RuntimeError(f"Failed to acquire token: {result}")
        self._token_cache[tenant.tenant_id] = {
            "token": token,
            "expires_at": datetime.utcnow() + timedelta(seconds=result.get("expires_in", 3500)),
        }
        return token

    def _client(self, tenant: TenantConfig) -> httpx.AsyncClient:
        token = self._acquire_token(tenant)
        headers = {"Authorization": f"Bearer {token}"}
        return httpx.AsyncClient(base_url="https://graph.microsoft.com/v1.0", headers=headers, timeout=30)

    async def get_users(self, tenant: TenantConfig) -> Dict:
        async with self._client(tenant) as client:
            response = await client.get("/users?$select=id,displayName,mail,userPrincipalName,accountEnabled")
            response.raise_for_status()
            return response.json()

    async def create_user(self, tenant: TenantConfig, payload: Dict) -> Dict:
        async with self._client(tenant) as client:
            response = await client.post("/users", json=payload)
            response.raise_for_status()
            return response.json()

    async def assign_license(self, tenant: TenantConfig, user_id: str, payload: Dict) -> Dict:
        async with self._client(tenant) as client:
            response = await client.post(f"/users/{user_id}/assignLicense", json=payload)
            response.raise_for_status()
            return response.json()
