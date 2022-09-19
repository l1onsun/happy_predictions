from fastapi import FastAPI

from happy_predictions.env import Env
from happy_predictions.factories import service_factories
from happy_predictions.service_provider.service_provider import ServiceProvider

app = ServiceProvider(services={Env: Env()}, factories=service_factories).solve(FastAPI)
