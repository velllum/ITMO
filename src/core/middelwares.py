from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from src.core.configs import settings


def register_middleware(app):
    """- регистрация промежуточного программного ПО """
    app.add_middleware(CORSMiddleware, allow_origins=settings.WEB_ALLOW_ORIGINS, allow_credentials=True,
                       allow_methods=["*"], allow_headers=["*"],)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.WEB_ALLOW_HOSTS.split())