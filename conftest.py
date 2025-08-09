import pytest

from faker import Faker
from fastapi.testclient import TestClient

from app import get_app


@pytest.fixture(scope="module")
def client():
    with TestClient(get_app()) as client:
        yield client


@pytest.fixture(scope="session")
def fake():
    Faker.seed(0)

    return Faker('es_MX')
