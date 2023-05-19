from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import PROJECT_HOST, PROJECT_PORT

from db.db import get_session
from models.base import Url
from schemas import base as schema
from services.base import url_crud

SHORT_URL_PATTERN = f'http://{PROJECT_HOST}:{PROJECT_PORT}/api/v1/'
router = APIRouter()


@router.post('/', response_model=schema.ShortUrlWithOrigin, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    url_in: schema.CreateShortUrl,
    db: AsyncSession = Depends(get_session),
) -> dict:
    url: Url = await url_crud.get_or_create(db=db, obj_in=url_in)
    return {
        'short_url': f'{SHORT_URL_PATTERN}{url.id}',
        'original_url': url.original_url
    }


@router.post('/shorten/', response_model=List[schema.ShortUrlWithId], status_code=status.HTTP_201_CREATED)
async def bulk_create_short_url(
    urls_in: List[schema.CreateShortUrl],
    db: AsyncSession = Depends(get_session),
) -> list:
    url_objects = [await url_crud.get_or_create(db=db, obj_in=url) for url in urls_in]
    result = [
        {'short_id': url.id, 'short_url': f'{SHORT_URL_PATTERN}{url.id}'} for url in url_objects
    ]
    return result


@router.get("/{id}/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_original_url(
    *,
    db: AsyncSession = Depends(get_session),
    id: int,
    response: Response
) -> None:
    """
    Get by ID.
    """
    url: Optional[Url] = await url_crud.get(db=db, id=id)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Url with {id} not found'
        )
    
    url.number_of_use += 1
    await db.commit()
    response.headers['Location'] = url.original_url
    return 


@router.get("/{id}/status", response_model=schema.ShortUrlStatic)
async def get_url_statistic(
    *,
    db: AsyncSession = Depends(get_session),
    id: int
) -> Any:
    """
    Get by ID.
    """
    url: Optional[Url] = await url_crud.get(db=db, id=id)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Url with {id} not found'
        )
    
    return {
        'short_url': f'{SHORT_URL_PATTERN}{url.id}',
        'original_url': url.original_url,
        'use': url.number_of_use,
    }
    