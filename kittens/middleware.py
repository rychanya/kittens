"""Middlewares"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class DBSession(BaseHTTPMiddleware):
    """DB session middleware"""

    def __init__(self, app, db_client) -> None:
        super().__init__(app)
        self._db_client = db_client

    async def dispatch(self, request: Request, call_next):
        request.state.db_client = self._db_client
        return await call_next(request)
