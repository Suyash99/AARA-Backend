import json
from fastapi import HTTPException
from starlette import status
from starlette.responses import JSONResponse
from typing import TypeVar
import logging

from app.mapper.serverResponseMapper import ServerResponse

T = TypeVar('T')

logger = logging.getLogger("main")


def handle_operation(result: T):
    try:
        return JSONResponse(
            content=json.loads(
                ServerResponse(
                    status_code=status.HTTP_200_OK,
                    error_messages=[],
                    error_message=None,
                    payload=result,
                    is_success=True
                ).model_dump_json()
            ),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as exception:
        logger.error(f"[Expected] [{exception.__class__.__name__}] exception={str(exception)}")
        return JSONResponse(
            content=json.loads(
                ServerResponse(
                    is_success=False,
                    status_code=exception.status_code,
                    payload=None,
                    error_message=str(exception.detail),
                    error_messages=[],
                )
            ),
            status_code=exception.status_code
        )
    except Exception as exception:
        logger.error(f"[Unexpected] [{exception.__class__.__name__}] exception={str(exception)}")
        return JSONResponse(
            content=json.loads(
                ServerResponse(
                    is_success=False,
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    error_message="Some error occurred",
                    error_messages=[],
                    payload=None
                ).model_dump_json()
            ),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
