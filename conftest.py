import pytest

from faker import Faker
from httpx import ASGITransport, AsyncClient

from app import get_app


@pytest.fixture
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=get_app()),
            base_url="http://localhost:8000"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
def fake():
    Faker.seed(0)

    return Faker('es_MX')
