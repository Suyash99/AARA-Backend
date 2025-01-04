from fastapi import HTTPException
from starlette import status
from starlette.responses import JSONResponse
import logging

logger = logging.getLogger("main")

def handle_operation(result):
    try:
        return JSONResponse(
            content={
                "is_success": True,
                "status_code": status.HTTP_200_OK,
                "payload": result,
                "error_message": None,
                "error_messages": []
            },
            status_code=status.HTTP_200_OK
        )
    except HTTPException as exception:
        logger.error(f"[Expected] [{exception.__class__.__name__}] exception={str(exception)}")
        return JSONResponse(
            content={
                "is_success": False,
                "status_code": exception.status_code,
                "error_message": str(exception.detail),
                "error_messages": [],
                "payload": None
            },
            status_code=exception.status_code
        )
    except Exception as exception:
        logger.error(f"[Unexpected] [{exception.__class__.__name__}] exception={str(exception)}")
        return JSONResponse(
            content={
                "is_success": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error_message": "Some error occurred",
                "error_messages": [],
                "payload": None
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
