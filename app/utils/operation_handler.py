import logging
from typing import TypeVar

from fastapi import HTTPException, status

from app.exceptions.response_exception import ResponseException
from app.mapper.serverResponseMapper import ServerResponse

T = TypeVar('T')

logger = logging.getLogger("main")


def handle_operation(operation):
    try:
        result = operation()
        return ServerResponse(
            status_code=status.HTTP_200_OK,
            error_messages=[],
            error_message=None,
            payload=result,
            is_success=True
        )
    except ResponseException as exception:
        logger.error(f"[Expected] [{exception.__class__.__name__}] Exception={str(exception)}")
        return ServerResponse(
            is_success=False,
            status_code=exception.status_code,
            payload=None,
            error_message=str(exception.message),
            error_messages=[],
        )

    except HTTPException as exception:
        logger.error(f"[Expected] [{exception.__class__.__name__}] Exception={str(exception)}")
        return ServerResponse(
            is_success=False,
            status_code=exception.status_code,
            payload=None,
            error_message=str(exception.detail),
            error_messages=[],
        )
    except Exception as exception:
        logger.error(f"[Unexpected] [{exception.__class__.__name__}] Exception={str(exception)}")
        return ServerResponse(
            is_success=False,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message="Some error occurred",
            error_messages=[],
            payload=None
        )
