from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas import base
from services.base import url_crud

router = APIRouter()


@router.post('/', response_model=base.ShortUrl, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    url_in: base.CreateShortUrl,
    db: AsyncSession = Depends(get_session),
):
    url = await url_crud.create(db=db, obj_in=url_in)
    return {
        'short_url': url.short_url,
        'original_url': url.original_url
    }


@router.get("/{id}")
async def get_original_url(
    *,
    db: AsyncSession = Depends(get_session),
    id: int,
) -> Any:
    """
    Get by ID.
    """
    entity = {}
    # get entity from db
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return entity


@router.get("/{id}/status")
async def get_url_stitistic(
    *,
    db: AsyncSession = Depends(get_session),
    id: int,
) -> Any:
    """
    Get by ID.
    """
    entity = {}
    # get entity from db
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return entity