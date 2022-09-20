import httpx
import pytest_asyncio
from fastapi import FastAPI


@pytest_asyncio.fixture
async def app_client(fastapi: FastAPI) -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=fastapi, base_url="http://app_test") as client:
        yield client
