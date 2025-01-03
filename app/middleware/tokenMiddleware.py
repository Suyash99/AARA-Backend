from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.utils.passwordUtils import PasswordUtils
from app.exceptions.tokenException import TokenException
from app.mapper.serverResponseMapper import ServerResponse
from app.utils.operationHandler import handle_operation
import logging

logger = logging.getLogger("main")

class TokenInterceptorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            # Retrieve the token from the request header
            token = request.headers.get("Authorization")
            if not token:
                raise TokenException("Missing or invalid token format", 401)

            PasswordUtils.verify_hashed_token(token)
        except TokenException as e:
            logger.error(f"TokenException: {str(e)}")
            return handle_operation(
                ServerResponse(
                    is_success=False,
                    status_code=e.status_code,
                    error_message=str(e)
                )
            )

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return handle_operation(
                ServerResponse(
                    is_success=False,
                    status_code=500,
                    error_message="An unexpected error occurred."
                )
            )

        # Proceed to the next middleware or endpoint
        response = await call_next(request)
        return response
