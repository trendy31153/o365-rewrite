from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select

from .graph import GraphClient
from .models import (
    AppReport,
    DirectoryUser,
    InviteCode,
    LicenseAssignment,
    LocalAccount,
    SystemSetting,
    TenantConfig,
)
from .security import hash_password


def _get_tenant_or_404(session: Session, tenant_id: int) -> TenantConfig:
    tenant = session.get(TenantConfig, tenant_id)
    if tenant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    return tenant


class TenantService:
    def __init__(self, session: Session):
        self.session = session

    def list(self) -> List[TenantConfig]:
        return list(self.session.exec(select(TenantConfig)))

    def create(self, tenant: TenantConfig) -> TenantConfig:
        if tenant.is_default:
            for record in self.session.exec(select(TenantConfig)):
                record.is_default = False
                self.session.add(record)
        self.session.add(tenant)
        self.session.commit()
        self.session.refresh(tenant)
        return tenant

    def update(self, tenant_id: int, payload: TenantConfig) -> TenantConfig:
        tenant = _get_tenant_or_404(self.session, tenant_id)
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(tenant, field, value)
        if payload.is_default:
            for record in self.session.exec(select(TenantConfig)):
                record.is_default = False
                self.session.add(record)
        self.session.add(tenant)
        self.session.commit()
        self.session.refresh(tenant)
        return tenant

    def delete(self, tenant_id: int) -> None:
        tenant = _get_tenant_or_404(self.session, tenant_id)
        self.session.delete(tenant)
        self.session.commit()


class AccountService:
    def __init__(self, session: Session):
        self.session = session

    def authenticate(self, username: str, password: str) -> LocalAccount:
        account = self.session.get(LocalAccount, username)
        if account is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        from .security import verify_password

        if not verify_password(password, account.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return account

    def create(self, username: str, password: str, roles: Optional[List[str]] = None) -> LocalAccount:
        if self.session.get(LocalAccount, username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account exists")
        account = LocalAccount(username=username, hashed_password=hash_password(password), roles=roles or ["admin"])
        self.session.add(account)
        self.session.commit()
        return account


class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.graph = GraphClient(session)

    def list(self, tenant_id: int) -> List[DirectoryUser]:
        tenant = _get_tenant_or_404(self.session, tenant_id)
        return list(self.session.exec(select(DirectoryUser).where(DirectoryUser.tenant_id == tenant.tenant_id)))

    def create(self, tenant_id: int, user: DirectoryUser) -> DirectoryUser:
        tenant = _get_tenant_or_404(self.session, tenant_id)
        user.tenant_id = tenant.tenant_id
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def bulk_create(self, tenant_id: int, prefix: str, count: int, strategy: str = "random") -> List[DirectoryUser]:
        created: List[DirectoryUser] = []
        for index in range(count):
            suffix = token_urlsafe(5)[:5] if strategy == "random" else str(index + 1).zfill(3)
            upn = f"{prefix}{suffix}@example.com"
            created.append(
                self.create(
                    tenant_id,
                    DirectoryUser(
                        tenant_id="",
                        user_principal_name=upn,
                        display_name=upn.split("@")[0],
                        password=token_urlsafe(8),
                    ),
                )
            )
        return created

    def update_roles(self, tenant_id: int, user_id: int, roles: List[str]) -> DirectoryUser:
        user = self.session.get(DirectoryUser, user_id)
        if user is None or user.tenant_id != _get_tenant_or_404(self.session, tenant_id).tenant_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.roles = roles
        self.session.add(user)
        self.session.commit()
        return user

    def update_status(self, tenant_id: int, user_id: int, enabled: bool) -> DirectoryUser:
        user = self.session.get(DirectoryUser, user_id)
        if user is None or user.tenant_id != _get_tenant_or_404(self.session, tenant_id).tenant_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.enabled = enabled
        self.session.add(user)
        self.session.commit()
        return user

    def assign_license(self, tenant_id: int, user_id: int, sku_id: str) -> DirectoryUser:
        user = self.session.get(DirectoryUser, user_id)
        if user is None or user.tenant_id != _get_tenant_or_404(self.session, tenant_id).tenant_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if sku_id not in user.licenses:
            user.licenses.append(sku_id)
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, tenant_id: int, user_id: int) -> None:
        user = self.session.get(DirectoryUser, user_id)
        if user is None or user.tenant_id != _get_tenant_or_404(self.session, tenant_id).tenant_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        self.session.delete(user)
        self.session.commit()


class LicenseService:
    def __init__(self, session: Session):
        self.session = session

    def list(self, tenant_id: int) -> List[LicenseAssignment]:
        tenant = _get_tenant_or_404(self.session, tenant_id)
        return list(self.session.exec(select(LicenseAssignment).where(LicenseAssignment.tenant_id == tenant.tenant_id)))

    def upsert(self, tenant_id: int, licenses: List[LicenseAssignment]) -> List[LicenseAssignment]:
        tenant = _get_tenant_or_404(self.session, tenant_id)
        for existing in self.session.exec(select(LicenseAssignment).where(LicenseAssignment.tenant_id == tenant.tenant_id)):
            self.session.delete(existing)
        for item in licenses:
            item.tenant_id = tenant.tenant_id
            self.session.add(item)
        self.session.commit()
        return licenses


class InviteService:
    def __init__(self, session: Session):
        self.session = session

    def list(self, tenant_id: int) -> List[InviteCode]:
        tenant = _get_tenant_or_404(self.session, tenant_id)
        return list(self.session.exec(select(InviteCode).where(InviteCode.tenant_id == tenant.tenant_id)))

    def create(self, tenant_id: int, expires_in_hours: int = 24, max_usage: int = 1) -> InviteCode:
        tenant = _get_tenant_or_404(self.session, tenant_id)
        code = InviteCode(
            tenant_id=tenant.tenant_id,
            code=token_urlsafe(16),
            expires_at=datetime.utcnow() + timedelta(hours=expires_in_hours),
            max_usage=max_usage,
        )
        self.session.add(code)
        self.session.commit()
        self.session.refresh(code)
        return code

    def redeem(self, code: str) -> InviteCode:
        invite = self.session.exec(select(InviteCode).where(InviteCode.code == code)).first()
        if invite is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
        if invite.expires_at < datetime.utcnow() or invite.used_count >= invite.max_usage:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invite expired")
        invite.used_count += 1
        self.session.add(invite)
        self.session.commit()
        return invite


class ReportService:
    def __init__(self, session: Session):
        self.session = session

    def snapshot(self, tenant_id: int) -> AppReport:
        tenant = _get_tenant_or_404(self.session, tenant_id)
        users = list(self.session.exec(select(DirectoryUser).where(DirectoryUser.tenant_id == tenant.tenant_id)))
        admins = list(
            self.session.exec(
                select(DirectoryUser).where(
                    DirectoryUser.tenant_id == tenant.tenant_id, DirectoryUser.roles.contains(["admin"])
                )
            )
        )
        report = AppReport(
            tenant_id=tenant.tenant_id,
            totals={"users": len(users), "admins": len(admins)},
            issues=[] if admins else ["No admins present"],
        )
        self.session.add(report)
        self.session.commit()
        self.session.refresh(report)
        return report

    def list(self, tenant_id: int) -> List[AppReport]:
        tenant = _get_tenant_or_404(self.session, tenant_id)
        return list(self.session.exec(select(AppReport).where(AppReport.tenant_id == tenant.tenant_id)))


class SettingService:
    def __init__(self, session: Session):
        self.session = session

    def list(self) -> List[SystemSetting]:
        return list(self.session.exec(select(SystemSetting)))

    def update(self, key: str, value: str, description: Optional[str] = None) -> SystemSetting:
        setting = self.session.get(SystemSetting, key) or SystemSetting(key=key, value=value, description=description)
        setting.value = value
        setting.description = description
        self.session.add(setting)
        self.session.commit()
        return setting
