from fastapi.testclient import TestClient


def test_main_again(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
