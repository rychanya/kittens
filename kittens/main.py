"""Fastapi app"""
from fastapi import Depends, FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from kittens import dependencies
from kittens.middleware import DBSession
from kittens.store import Store


def create_app():
    """app fabric method"""
    _db_client = AsyncIOMotorClient()
    _app = FastAPI()
    _app.add_middleware(DBSession, db_client=_db_client)

    @_app.get("/")
    async def root(store: Store = Depends(dependencies.store)):
        res = await store.answers.insert_one({"a": "b"})
        return str(res)

    return _app


app = create_app()
