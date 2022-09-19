import httpx
import pytest
from fastapi import FastAPI


@pytest.fixture
async def app_client(fastapi: FastAPI) -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=fastapi, base_url="app_test") as client:
        yield client
