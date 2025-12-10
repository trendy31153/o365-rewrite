from datetime import datetime
from typing import Dict, List, Optional

from sqlmodel import JSON, Column, Field, SQLModel


class TenantConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str
    tenant_id: str
    client_id: str
    client_secret: str
    authority_host: str = "https://login.microsoftonline.com"
    scopes: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    is_default: bool = False
    notes: Optional[str] = None


class DirectoryUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: str = Field(index=True)
    user_principal_name: str = Field(index=True)
    display_name: str
    password: Optional[str] = None
    enabled: bool = True
    roles: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    licenses: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LicenseAssignment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: str = Field(index=True)
    sku_id: str
    friendly_name: str
    available: int = 0
    assigned: int = 0


class InviteCode(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: str = Field(index=True)
    code: str = Field(index=True)
    expires_at: datetime
    max_usage: int = 1
    used_count: int = 0
    allowed_roles: List[str] = Field(default_factory=list, sa_column=Column(JSON))


class SystemSetting(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str
    description: Optional[str] = None


class AppReport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: str = Field(index=True)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    totals: Dict[str, int] = Field(default_factory=dict, sa_column=Column(JSON))
    issues: List[str] = Field(default_factory=list, sa_column=Column(JSON))


class LocalAccount(SQLModel, table=True):
    username: str = Field(primary_key=True)
    hashed_password: str
    roles: List[str] = Field(default_factory=lambda: ["admin"], sa_column=Column(JSON))
