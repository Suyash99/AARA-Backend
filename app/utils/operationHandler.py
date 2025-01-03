from fastapi import HTTPException
from typing import TypeVar
from starlette import status
from app.mapper.serverResponseMapper import ServerResponse
from fastapi.exceptions import RequestValidationError
import socket
from urllib.error import URLError
import logging

T = TypeVar('T')

logger = logging.getLogger('main')

def handle_operation(result: T) -> ServerResponse[T]:
    try:
        return ServerResponse(
            is_success=True,
            status_code=status.HTTP_200_OK,
            payload=result
        )

    except HTTPException as exception:
        logger.error(f"[Expected] [{exception.__class__.__name__}] exception={str(exception)}")
        return ServerResponse(
            is_success=False,
            status_code=exception.status_code,
            error_message=str(exception.detail)
        )

    except RequestValidationError as exception:
        logger.error(f"[Expected] [{exception.__class__.__name__}] exception={str(exception)}")
        return ServerResponse(
            is_success=False,
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            error_message=str(exception)
        )

    except (URLError, socket.timeout) as exception:
        logger.error(f"[Expected] [{exception.__class__.__name__}] exception={str(exception)}")
        message = "Request timed out" if isinstance(exception, socket.timeout) else "Resource unavailable"
        return ServerResponse(
            is_success=False,
            status_code=status.HTTP_REQUEST_TIMEOUT,
            error_message=message
        )

    except ValueError as exception:
        logger.error(f"[Expected] [{exception.__class__.__name__}] exception={str(exception)}")
        return ServerResponse(
            is_success=False,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_message=str(exception)
        )

    except Exception as exception:
        logger.error(f"[Unexpected] [{exception.__class__.__name__}] exception={str(exception)}")
        return ServerResponse(
            is_success=False,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message="Some error occurred"
        )