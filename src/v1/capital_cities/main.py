import logging

import uvicorn

from src.core.configs import settings
from src.v1 import create_app

logger = logging.getLogger(__name__)

app = create_app()


if __name__ == "__main__":
    uvicorn.run('src.v1.capital_cities.main:app',  host=settings.WEB_HOST, port=settings.WEB_PORT,
                reload=settings.WEB_RELOAD, log_config='src/core/logging.conf',)

