import os

from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.httpx import HttpxIntegration

load_dotenv()


def init_sentry() -> None:
    sentry_dsn = os.getenv("SENTRY_DSN", None)

    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[
                HttpxIntegration(),
            ],
        )
