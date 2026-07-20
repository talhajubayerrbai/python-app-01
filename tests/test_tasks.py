import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_list_tasks_empty(client):
    response = await client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_task(client):
    payload = {"title": "Buy groceries", "description": "Milk, eggs, bread"}
    response = await client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["completed"] is False
    assert "id" in data


@pytest.mark.asyncio
async def test_get_task(client):
    create_resp = await client.post("/tasks", json={"title": "Read a book"})
    task_id = create_resp.json()["id"]

    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read a book"


@pytest.mark.asyncio
async def test_update_task(client):
    create_resp = await client.post("/tasks", json={"title": "Write code"})
    task_id = create_resp.json()["id"]

    response = await client.put(f"/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


@pytest.mark.asyncio
async def test_delete_task(client):
    create_resp = await client.post("/tasks", json={"title": "Clean house"})
    task_id = create_resp.json()["id"]

    del_resp = await client.delete(f"/tasks/{task_id}")
    assert del_resp.status_code == 204

    get_resp = await client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_get_task_not_found(client):
    response = await client.get("/tasks/999999")
    assert response.status_code == 404
