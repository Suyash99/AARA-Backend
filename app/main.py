from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.token_middleware import TokenInterceptorMiddleware
from app.routes.tokenRoutes import router as tokenRoutes
from app.routes.userRoutes import router as userRoutes
import uvicorn

from app.utils.constants import SERVER_IP, SERVER_PORT


def create_app() -> FastAPI:
    app = FastAPI(
        title="AARA-Backend",
        description="Backend for AARA",
        version="0.0.1",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #Middlewares
    app.add_middleware(TokenInterceptorMiddleware)

    #Routes
    app.include_router(tokenRoutes)
    app.include_router(userRoutes)

    return app

def main():
    """
    The main entry point for the application.
    """
    app = create_app()
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)

if __name__ == "__main__":
    main()
