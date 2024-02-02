import uvicorn
from config import Envs


def main():
    uvicorn.run(
        app="api.server:app",
        host=Envs.APP_HOST,
        port=Envs.APP_PORT,
        reload=True if Envs.ENV != "PROD" else False,
        workers=2,
        log_config="log_config.yaml"
    )


if __name__ == "__main__":
    main()
