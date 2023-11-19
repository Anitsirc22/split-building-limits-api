import logging

from typing import Any, Awaitable, Callable

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.exceptions import (
    InputGeometryError,
    InputValueError,
    SplitBuildingLimitsNotFoundError,
)


logger = logging.getLogger(__name__)


async def input_geometry_error_handler(_: Request, exc: InputGeometryError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"{exc!s}"},
    )


async def input_value_error_handler(_: Request, exc: InputValueError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"{exc!s}"},
    )


async def split_building_limits_not_found_handler(_: Request, exc: SplitBuildingLimitsNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"{exc!s}"},
    )


async def catchall_exceptions_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Any]]
) -> Awaitable[Any] | JSONResponse:
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(f"Something went wrong. error={e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Something went wrong."},  # don't show the error to the user
        )
