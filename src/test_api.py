import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core import config
from db.db import Base, get_session
from main import app

SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5433/postgres'
TEST_URL_1 = 'https://ya.ru/'
TEST_URL_2 = 'https://yandex.ru/'


async def override_get_session() -> AsyncSession:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture()
def get_client():
    client = TestClient(app)
    return client


def test_url_creation(get_client):
    data = {
        'original_url': TEST_URL_1
    }
    response = get_client.post('/api/v1/', json=data)

    assert response.status_code == 201
    response_message = {
        'short_url': f'http://{config.PROJECT_HOST}:{config.PROJECT_PORT}/api/v1/1',
        'original_url': TEST_URL_1
    }
    assert response.json() == response_message


def test_bulk_creation(get_client):
    data = [
        {
            'original_url': TEST_URL_1
        },
        {
            'original_url': TEST_URL_2
        }
    ]

    response = get_client.post('/api/v1/shorten', json=data)
    
    assert response.status_code == 201
    response_message = [
        {
            'short_url': f'http://{config.PROJECT_HOST}:{config.PROJECT_PORT}/api/v1/1',
            'short_id': 1
        },
        {
            'short_url': f'http://{config.PROJECT_HOST}:{config.PROJECT_PORT}/api/v1/2',
            'short_id': 2
        }
    ]
    assert response.json() == response_message
