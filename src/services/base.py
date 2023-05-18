import uuid
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from db.db import Base
from models.base import Url
from schemas.base import CreateShortUrl


class Repository:

    def get(self, *args, **kwargs):
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
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> Url:
        url_dict: dict = jsonable_encoder(obj_in)
        print(url_dict)
        original_url: str = url_dict.get('url')
        if not original_url:
            raise Exception


        url = {
            'original_url': original_url,
            'short_url': uuid.uuid4().hex[:10],
        }    

        db_obj = self._model(**url)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


url_crud = RepositoryShortUrl(Url) 