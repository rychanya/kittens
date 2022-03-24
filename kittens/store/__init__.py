"""Store"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from kittens.store.settings import StoreSettings


class Store:
    """Store"""

    def __init__(self, db_client: AsyncIOMotorClient, settings: StoreSettings) -> None:
        self.settings = settings
        self.db_client = db_client

    def _get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        return self.db_client.get_database(self.settings.db_name).get_collection(
            collection_name
        )

    @property
    def answers(self):
        """answers collection"""
        return self._get_collection("answers")
