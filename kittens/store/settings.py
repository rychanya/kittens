"""Store settings"""

from pydantic import BaseSettings


class StoreSettings(BaseSettings):
    """Store Settings"""
    db_name: str = "Агуа"
