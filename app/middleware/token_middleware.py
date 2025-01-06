import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse
from app.utils.constants import APP_ID, API_VERSION

from app.exceptions.tokenException import TokenException
from app.utils.crypto_utils import PasswordUtils

logger = logging.getLogger("main")


class TokenInterceptorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            # Skip token check for create user flow
            if not (
                    (request.url.path.rstrip('/') == f"/{APP_ID}/{API_VERSION}/user" and
                    request.method == 'POST') or
                    (request.url.path.rstrip("/") == f"/{APP_ID}/{API_VERSION}/user/re-login" and
                    request.method == "PUT")
            ):
                token = request.headers.get("Authorization")
                if not token:
                    raise TokenException("Missing token in request", 401)

                PasswordUtils.verify_hashed_token(token)

        except TokenException as e:
            logger.error(f"TokenException: {str(e)}")
            return JSONResponse(
                content={
                    "is_success": False,
                    "status_code": e.status_code,
                    "error_message": str(e),
                    "error_messages": [],
                    "payload": {}
                },
                status_code=e.status_code
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JSONResponse(
                content={
                    "is_success": False,
                    "status_code": 500,
                    "error_message": "An unexpected error occurred.",
                    "error_messages": [],
                    "payload": {}
                },
                status_code=500
            )

        response = await call_next(request)
        return response
