from sqlmodel import Session, SQLModel, create_engine

from .config import get_settings
from .models import AppReport, DirectoryUser, InviteCode, LicenseAssignment, LocalAccount, SystemSetting, TenantConfig

settings = get_settings()
engine = create_engine(settings.database_url, echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        if session.get(LocalAccount, "admin") is None:
            from passlib.context import CryptContext

            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            session.add(
                LocalAccount(
                    username="admin",
                    hashed_password=pwd_context.hash("admin"),
                    roles=["admin"],
                )
            )
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session
