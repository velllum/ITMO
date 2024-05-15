import logging

import uvicorn


from . import create_app, settings


logger = logging.getLogger(__name__)

app = create_app()


if __name__ == "__main__":
    uvicorn.run('src.main_capital_cities:app',
                host=settings.WEB_HOST,
                port=settings.WEB_PORT,
                reload=settings.WEB_RELOAD,
                log_config='src/core/logging.conf',)

