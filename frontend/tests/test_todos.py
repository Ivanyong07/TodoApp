import pytest #pytest framework
from httpx import ASGITransport, AsyncClient
#async client is fake http, asgi transport is connewct direct to out fastapi
from todo.models import User, Todo
from todo.users import current_active_user
from todo.app import app
from uuid import uuid4
from todo.db import engine, AsyncSessionLocal

def test_addition():
    assert 1 + 1 == 2
#The test below is an asynchronous test. Run it using asyncio

@pytest.mark.asyncio
async def test_testing_endpoint():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/testing") #create testing
    
    assert response.status_code == 200
    assert response.json() == {"message":"Hello World"}

@pytest.mark.asyncio
async def test_get_todos():
    fake_user = User(
        id=uuid4(),
        email="test1@example.com",
        hashed_password="fake",
        is_active=True,
        is_superuser=False,
        is_verified=True
    )

    async def override_current_user():
        return fake_user

    app.dependency_overrides[current_active_user] = override_current_user

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.get("/uploads")
    
    assert response.status_code == 200
    assert "todos" in response.json()

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_post_todos():
    fake_user = User(
        id=uuid4(),
        email="test_test11@example.com",
        hashed_password="fake",
        is_active=True,
        is_superuser=False,
        is_verified=True
    )
    async with AsyncSessionLocal() as session:
        session.add(fake_user)
        await session.commit()

    async def override_current_user():
        return fake_user

    app.dependency_overrides[current_active_user] = override_current_user

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/uploads",
            json={
                "title":"Testing 1",
                "description":"First test for create todo",
                "completed":False
            }
        )

    assert response.status_code == 200
    assert "id" in response.json()

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_delete_todos():
    fake_user = User(
        id=uuid4(),
        email="delete_test21@example.com",
        hashed_password="fake",
        is_active=True,
        is_superuser=False,
        is_verified=True
    )

    fake_todo = Todo(
        id=uuid4(),
        user_id=fake_user.id,
        title="Testing",
        description="First test for create todo",
        completed=False
    )

    async with AsyncSessionLocal() as session:
        session.add(fake_user)
        session.add(fake_todo)
        await session.commit()

    async def override_current_user():
        return fake_user
    
    app.dependency_overrides[current_active_user] = override_current_user

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.delete(
            f"/uploads/{fake_todo.id}"
        )

    assert response.status_code == 200
    assert "ID" in response.json()

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_put_todos():
    fake_user = User(
        id=uuid4(),
        email="put_test21@example.com",
        hashed_password="fake",
        is_active=True,
        is_superuser=False,
        is_verified=True
    )

    fake_todo = Todo(
        id=uuid4(),
        user_id=fake_user.id,
        title="Testing 1",
        description="First test for create todo",
        completed=False
    )

    async def override_current_user():
        return fake_user

    app.dependency_overrides[current_active_user] = override_current_user

    async with AsyncSessionLocal() as session:
        session.add(fake_todo)
        session.add(fake_user)

        await session.commit()
    

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.put(
            f"/uploads/{fake_todo.id}",
            json={
                "title":"Testing put",
                "description":"First test for put todo",
                "completed":True
            }
        )
    
    assert response.status_code == 200
    assert "ID" in response.json()

    app.dependency_overrides.clear()




   