from typing import Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import Base
from exceptions.base import FieldError
from models.base import Url
from schemas.base import CreateShortUrl


class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError
    
    def get_or_create(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError
    

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel) 


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model 
 

class RepositoryShortUrl(RepositoryDB[Url, CreateShortUrl]):
    async def get_or_create(
            self, db: AsyncSession, *, obj_in: CreateSchemaType
        ) -> Url:
        url_dict: dict = jsonable_encoder(obj_in)
        original_url: str = url_dict.get('original_url')
        if not original_url:
            raise FieldError(field='original_url')
        
        db_obj: Optional[Url] = await self.get(db=db, original_url=original_url)
        if db_obj:
            return db_obj   

        db_obj = self._model(**url_dict)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    

    async def get(
            self,
            db: AsyncSession,
            id: Optional[int] = None,
            original_url: Optional[str] = None
        ) -> Optional[Url]:
        if not id and not original_url:
            raise FieldError(field='id or original_url')
        if id:
            statement = select(self._model).where(self._model.id == id)
        if original_url:
            statement = select(self._model) \
                        .where(self._model.original_url == original_url)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()


url_crud = RepositoryShortUrl(Url) 