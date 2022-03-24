"""Dependencies"""
from fastapi import Depends, Request
from motor.motor_asyncio import AsyncIOMotorClient

from kittens.store import Store
from kittens.store.settings import StoreSettings

store_settings = StoreSettings()


def db_client(request: Request) -> AsyncIOMotorClient:
    """Motor client"""
    return request.state.db_client


def store(_db_client=Depends(db_client)) -> Store:
    """Store"""
    return Store(_db_client, store_settings)
