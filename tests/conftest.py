from os import environ
from typing import Optional

import pytest
from _pytest.mark import Mark
from fastapi import FastAPI

from happy_predictions.env import Env
from happy_predictions.factories import service_factories
from happy_predictions.service_provider.service_provider import ServiceProvider
from happy_predictions.service_provider.types import Service, ServiceClass
from happy_predictions.telegram.telegram_service import TelegramService


@pytest.fixture
def env():
    return Env(
        mongo_uri=environ.get("TEST_MONGO_URI")
        or "mongodb://localhost:27017/happy_predictions_test",
        telegram_api_token="fake_telegram_api_token",
        bot_host="localhost",
        debug=True,
    )


@pytest.fixture
def service_provider(request, env: Env):
    marker: Optional[Mark] = request.node.get_closest_marker("provider_override")
    override_services: dict[ServiceClass, Service] = marker.args[0] if marker else {}
    service_provider = ServiceProvider(
        services={Env: env} | override_services, factories=service_factories
    )
    service_provider.solve_all()
    return service_provider


@pytest.fixture
def fastapi(service_provider: ServiceProvider) -> FastAPI:
    return service_provider.provide(FastAPI)


@pytest.fixture
def telegram(service_provider: ServiceProvider) -> TelegramService:
    return service_provider.provide(TelegramService)


# @pytest.fixture
# def telegram(service_provider: ServiceProvider) -> TelegramService:
#     return service_provider.provide(TelegramService
