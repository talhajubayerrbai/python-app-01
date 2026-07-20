import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_list_todos_empty(client):
    response = await client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_todo(client):
    payload = {"title": "Buy groceries", "description": "Milk, eggs, bread"}
    response = await client.post("/todos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["completed"] is False
    assert "id" in data


@pytest.mark.asyncio
async def test_get_todo(client):
    create_resp = await client.post("/todos", json={"title": "Read a book"})
    todo_id = create_resp.json()["id"]

    response = await client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read a book"


@pytest.mark.asyncio
async def test_update_todo(client):
    create_resp = await client.post("/todos", json={"title": "Write code"})
    todo_id = create_resp.json()["id"]

    response = await client.put(f"/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


@pytest.mark.asyncio
async def test_delete_todo(client):
    create_resp = await client.post("/todos", json={"title": "Clean house"})
    todo_id = create_resp.json()["id"]

    del_resp = await client.delete(f"/todos/{todo_id}")
    assert del_resp.status_code == 204

    get_resp = await client.get(f"/todos/{todo_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_get_todo_not_found(client):
    response = await client.get("/todos/999999")
    assert response.status_code == 404
