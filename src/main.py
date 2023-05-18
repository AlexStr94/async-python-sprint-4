import uvicorn
from fastapi import FastAPI

from api.v1 import base
from core import config


app = FastAPI(
    title=config.app_settings.app_title,
)
app.include_router(base.router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
    ) 