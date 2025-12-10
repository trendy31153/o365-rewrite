from fastapi import APIRouter, HTTPException, Query

from app import models
from app.services.user_service import user_service
from app.services.license_service import license_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[models.User])
async def list_users(keyword: str | None = None, limit: int = Query(50, le=200)):
    if keyword:
        return await user_service.search_users(keyword, limit)
    return await user_service.list_users()


@router.post("", response_model=models.User, status_code=201)
async def create_user(payload: models.CreateUserRequest):
    return await user_service.create_user(payload)


@router.post("/bulk", response_model=list[models.User], status_code=201)
async def bulk_create(request: models.BulkUserRequest):
    return await user_service.bulk_create(request)


@router.patch("/{user_id}", response_model=models.User)
async def update_user(user_id: str, payload: models.UpdateUserRequest):
    return await user_service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str):
    await user_service.delete_user(user_id)


@router.get("/{user_id}/password", response_model=str)
async def default_password(user_id: str):
    return await user_service.default_password(user_id)


@router.post("/{user_id}/licenses", response_model=list[str])
async def assign_license(user_id: str, sku_ids: list[str]):
    return await license_service.assign(user_id, sku_ids)


@router.get("/roles", response_model=list[str])
async def available_roles():
    return await user_service.get_roles()
