from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import userRoutes
import uvicorn
from app.appConstants import SERVER_CONFIG


def create_app() -> FastAPI:
    app = FastAPI(
        title="AARA-Backend",
        description="Backend for AARA",
        version="0.0.1",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Replace with specific origins in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(userRoutes, prefix="/users", tags=["Users"])

    return app

def main():
    """
    The main entry point for the application.
    """
    app = create_app()
    uvicorn.run(app, host=SERVER_CONFIG['SERVER_URL'], port=SERVER_CONFIG['SERVER_PORT'])

if __name__ == "__main__":
    main()
