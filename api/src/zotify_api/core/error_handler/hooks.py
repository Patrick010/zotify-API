import asyncio
import logging
import sys
from typing import TYPE_CHECKING

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from .formatter import JsonFormatter

if TYPE_CHECKING:
    from . import ErrorHandler


log = logging.getLogger(__name__)

def _get_request_id(request: Request) -> str:
    """Safely get request_id from request state."""
    try:
        return request.state.request_id
    except AttributeError:
        return "N/A"

def register_fastapi_hooks(app: FastAPI, handler: "ErrorHandler"):
    """
    Registers a global exception handler for the FastAPI application.
    """
    log.info("Registering FastAPI exception handler.")
    json_formatter = JsonFormatter(verbosity=handler.config.verbosity)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        request_id = _get_request_id(request)
        context = {"request_id": request_id}

        # Process the exception (log, trigger actions, etc.)
        await handler.handle_exception_async(exc, context=context)

        # Format a clean response for the client
        response_data = json_formatter.format(exc, context=context)

        # For now, return a generic 500. In a real app, we might
        # map exception types to different status codes.
        return JSONResponse(status_code=500, content=response_data)

def register_system_hooks(handler: "ErrorHandler"):
    """
    Registers exception handlers for non-FastAPI contexts (e.g., background tasks).
    """
    log.info("Registering system-level exception handlers.")

    def sync_excepthook(exc_type, exc_value, exc_traceback):
        # This hook handles exceptions in the main thread and other non-async contexts
        if issubclass(exc_type, (KeyboardInterrupt, SystemExit)):
            # Don't intercept standard exit signals
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        handler.handle_exception(exc_value, context={"hook": "sys.excepthook"})

    def asyncio_exception_handler(loop, context):
        # This hook handles exceptions in asyncio tasks that are not awaited
        exception = context.get("exception")
        if exception:
            handler.handle_exception(exception, context={"hook": "asyncio"})
        else:
            log.warning(
                "Asyncio exception handler called without an exception.",
                extra=context
            )

    sys.excepthook = sync_excepthook

    try:
        loop = asyncio.get_running_loop()
        loop.set_exception_handler(asyncio_exception_handler)
    except RuntimeError:
        # No running loop, which is fine if the app is not async-first.
        # The handler will be set when a loop is created.
        log.info("No running asyncio loop found. Handler will be set on loop creation.")
        asyncio.get_event_loop().set_exception_handler(asyncio_exception_handler)
