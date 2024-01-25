import os
from fastapi import FastAPI
from api.controllers import router


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Locker",
        description="Locker Twilio API",
        version="1.0.0",
        debug=bool(int(os.getenv('DEBUG')))
    )
    init_routers(app_=app_)
    return app_


app = create_app()
