from fastapi import FastAPI
from src.controllers import router


def init_routers(app: FastAPI) -> None:
    app.include_router(router)


def main() -> FastAPI:
    _app = FastAPI(
        title="Api Fila Atendimento",
        description="Api destinada para funções de fila de atendimento",
        version="0.0.1",
    )
    init_routers(app=_app)
    return _app


app = main()

if __name__ == "__main__":
    main()
