from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    expires_at: datetime
    refresh_token: str | None = None


class User(BaseModel):
    id: str
    user_principal_name: EmailStr
    display_name: str
    given_name: str | None = None
    surname: str | None = None
    mobile_phone: str | None = None
    usage_location: str | None = None
    roles: list[str] = Field(default_factory=list)
    license_skus: list[str] = Field(default_factory=list)
    invited: bool = False
    status: Literal["active", "disabled", "pending"] = "active"


class CreateUserRequest(BaseModel):
    user_principal_name: EmailStr
    display_name: str
    password: str
    force_change_password_next_sign_in: bool = False
    license_skus: list[str] = Field(default_factory=list)
    usage_location: str | None = None


class UpdateUserRequest(BaseModel):
    display_name: str | None = None
    given_name: str | None = None
    surname: str | None = None
    mobile_phone: str | None = None
    usage_location: str | None = None
    roles: list[str] | None = None
    license_skus: list[str] | None = None


class LicensePlan(BaseModel):
    sku_id: str
    name: str
    enabled: bool = True
    available: int | None = None


class Invite(BaseModel):
    id: str
    email: EmailStr
    redeem_url: str
    created_at: datetime
    expires_at: datetime | None = None
    role: str | None = None
    redeemed: bool = False


class Domain(BaseModel):
    id: str
    name: str
    verified: bool = False
    default: bool = False


class Organization(BaseModel):
    id: str
    display_name: str
    tenant_id: str
    domains: list[Domain] = Field(default_factory=list)


class Report(BaseModel):
    type: Literal["exchange", "onedrive", "application"]
    content: dict
    generated_at: datetime


class SystemStatus(BaseModel):
    multi_tenant_enabled: bool = False
    invite_only_mode: bool = False
    allow_user_registration: bool = True


class BulkUserRequest(BaseModel):
    users: list[CreateUserRequest]
    license_sku: str | None = None


class SearchQuery(BaseModel):
    keyword: str
    limit: int = 10
