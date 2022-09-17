from fastapi import FastAPI

from happy_predictions.env import Env, parse_environment_values
from happy_predictions.factories import service_factories
from happy_predictions.service_provider.service_provider import ServiceProvider

app = ServiceProvider(
    services={Env: parse_environment_values()}, factories=service_factories
).solve(FastAPI)
