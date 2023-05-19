import uvicorn
from fastapi import Depends, FastAPI

from api.v1 import base
from core import config
from middlware.black_list import check_allowed_ip


app = FastAPI(
    title=config.app_settings.app_title,
    dependencies=[Depends(check_allowed_ip)]
)

app.include_router(base.router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
    ) 