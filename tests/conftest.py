"""Fixtures"""
import subprocess
from tempfile import TemporaryDirectory
import pytest


@pytest.fixture
def anyio_backend():
    """AnyIO fixture"""
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def start_mongo():
    """Fixture subprocess mongo"""
    with TemporaryDirectory() as tempdir:
        with subprocess.Popen(
            [
                "mongod",
                "--replSet",
                "rs0",
                "--dbpath",
                tempdir,
                "--bind_ip",
                "localhost",
            ],
            stdout=subprocess.DEVNULL,
        ) as mongo:
            subprocess.run(
                ["mongosh", "--eval", "rs.initiate()"],
                stdout=subprocess.DEVNULL,
                check=True,
            )

            yield

            mongo.terminate()
            mongo.wait()
