import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .core import settings, lifespan

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """- создаем приложение"""
    app = FastAPI(title="HTTP REST API", debug=settings.WEB_DEBUG, lifespan=lifespan)
    register_middleware(app)
    return app


def register_middleware(app):
    """- регистрация промежуточного программного ПО """
    app.add_middleware(CORSMiddleware,
                       allow_origins=settings.WEB_ALLOW_ORIGINS,
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"],)

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.WEB_ALLOW_HOSTS.split())


