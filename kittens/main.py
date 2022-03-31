"""Fastapi app"""
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from kittens.middleware import DBSession
from kittens.routers import questions


def create_app():
    """app fabric method"""
    _db_client = AsyncIOMotorClient(uuidRepresentation="standard")
    _app = FastAPI()
    _app.add_middleware(DBSession, db_client=_db_client)
    _app.include_router(router=questions.router, prefix="/api/question")

    return _app


app = create_app()
