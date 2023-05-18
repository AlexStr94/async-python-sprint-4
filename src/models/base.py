from sqlalchemy import Column, DateTime, ForeignKey, func, Integer, String
# Импортируем базовый класс для моделей.
from db.db import Base


class Url(Base):
    __tablename__ = "url"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    original_url = Column(String(1024), unique=True)
    short_url = Column(String(64), unique=True)
    number_of_use = Column(Integer, default=0)

    def __repr__(self):
        return f'Add {self.original_url}'