from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..models import SystemSetting
from ..security import require_admin
from ..services import SettingService

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("/", response_model=List[SystemSetting])
def list_settings(session: Session = Depends(get_session)) -> List[SystemSetting]:
    return SettingService(session).list()


@router.put("/{key}", response_model=SystemSetting)
def update_setting(key: str, payload: SystemSetting, session: Session = Depends(get_session)) -> SystemSetting:
    return SettingService(session).update(key, payload.value, payload.description)
