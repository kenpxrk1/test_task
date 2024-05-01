from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from api.db import get_async_session
from api.services.user import UserService
from .depends import get_user_service
from .schemas import UserReadDTO, UserСreateDTO
from sqlalchemy.exc import IntegrityError
from api.exc import UserAlreadyLockedError
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserReadDTO)
async def create_user(
    request: UserСreateDTO,
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_async_session),
) -> UserReadDTO:
    """
    creates a new user and returns success message if it
    done correctly
    """
    try:
        user = await service.create_user(request, session)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with that email already exist",
        )


@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserReadDTO | None])
async def get_users(
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_async_session),
) -> List[UserReadDTO | None]:
    """get method that returns a list of all users or empty list if they dont exist"""

    users = await service.get_users(session)
    return users


@router.patch(
    "/acquire_lock/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserReadDTO,
)
async def acquire_lock(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_async_session),
) -> UserReadDTO:
    """patch method that updates locktime status
    and returns UserReadDTO object
    """
    try:
        user = await service.acquire_lock(user_id, session)

    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does not exist :(",
        )

    except UserAlreadyLockedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with id: {user_id} already locked :(",
        )

    return user


@router.patch(
    "/release_lock/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserReadDTO,
)
async def release_lock(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_async_session),
) -> UserReadDTO:
    """patch method that resets locktime status
    and returns UserReadDTO object
    """
    try:
        user = await service.release_lock(user_id, session)

    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does not exist :(",
        )

    return user
