import pytest
from httpx import ASGITransport, AsyncClient

from todo.app import app

def test_addition():
    assert 1 + 1 == 2

@pytest.mark.asyncio
async def test_testing_endpoint():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/testing")
    
    assert response.status_code == 200
    assert response.json() == {"message":"Hello World"}


