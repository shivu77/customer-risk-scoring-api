from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.utils.logger import get_logger

logger = get_logger("app.exceptions")

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.exception(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "detail": exc.detail},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.exception("RequestValidationError")
    return JSONResponse(
        status_code=422,
        content={"status": "validation_error", "errors": exc.errors()},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled Exception")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": "Internal server error"},
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

