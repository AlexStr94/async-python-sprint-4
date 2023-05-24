import os
from logging import config as logging_config

from pydantic import BaseSettings, PostgresDsn

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))

class AppSettings(BaseSettings):
    app_title: str = os.getenv('PROJECT_NAME', 'UrlShortener')
    database_dsn: PostgresDsn
    project_host = os.getenv('PROJECT_HOST', '127.0.0.1')
    project_port = int(os.getenv('PROJECT_PORT', '8000'))
    api_v1_prefix = '/api/v1'
    short_url_pattern = f'http://{project_host}:{project_port}{api_v1_prefix}/' 
    black_list = os.getenv(
        'BLACK_LIST',
        default='',
    ).split(' ')

    class Config:
        env_file = '../.env'


app_settings = AppSettings() 