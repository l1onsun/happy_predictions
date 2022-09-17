from dataclasses import dataclass

import pytest

from happy_predictions.const import SECRET_STR
from happy_predictions.env import Env
from happy_predictions.service_provider.service_factory import ServiceFactories
from happy_predictions.service_provider.service_provider import ServiceProvider


@dataclass
class SomeServiceA:
    some_str: str


@dataclass
class SomeServiceB:
    a: SomeServiceA


@dataclass
class SomeServiceC:
    a: SomeServiceA
    b: SomeServiceB
    is_some: bool


service_factories = ServiceFactories()


@service_factories.add
def build_some_service_a(env: Env) -> SomeServiceA:
    return SomeServiceA(env.mongo_uri)


@service_factories.add
def build_some_service_b(a: SomeServiceA) -> SomeServiceB:
    return SomeServiceB(a)


@service_factories.add
def build_some_service_c(a: SomeServiceA, b: SomeServiceB) -> SomeServiceC:
    return SomeServiceC(a, b, is_some=True)


@pytest.mark.asyncio
async def test_provider_solve_all():
    provider = ServiceProvider(
        {SomeServiceA: SomeServiceA(SECRET_STR)}, service_factories
    )
    provider.solve_all()
    assert provider.services.keys() == {
        ServiceProvider,
        SomeServiceA,
        SomeServiceB,
        SomeServiceC,
    }
    assert provider.provide(SomeServiceC).a.some_str == SECRET_STR
