from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from api.services.user import UserService
from .depends import get_user_service
from .schemas import UserReadDTO, UserСreateDTO
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: UserСreateDTO, service: UserService = Depends(get_user_service)
):
    try:
        await service.create_user(request)
        return "user created successfully"
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with that email already exist",
        )
    
@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserReadDTO | None])
async def get_users(
    service: UserService = Depends(get_user_service)
) -> List[UserReadDTO | None]:
    users = await service.get_users()
    return users


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserReadDTO)
async def acquire_lock(
    user_id: UUID,
    service: UserService = Depends(get_user_service)
) -> UserReadDTO | None:
    user = await service.acquire_lock(user_id)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does not exist :("
        )
    return user
    
