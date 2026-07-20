from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
from app import crud

app = FastAPI(
    title="python-app-01",
    description="FastAPI todo list REST API",
    version="1.0.0",
)


@app.get("/health", tags=["ops"])
async def health():
    return {"status": "ok"}


@app.get("/todos", response_model=List[TodoResponse], tags=["todos"])
async def list_todos(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_todos(db, skip=skip, limit=limit)


@app.get("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED, tags=["todos"])
async def create_todo(todo_in: TodoCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_todo(db, todo_in)


@app.put("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
async def update_todo(
    todo_id: int, todo_in: TodoUpdate, db: AsyncSession = Depends(get_db)
):
    todo = await crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return await crud.update_todo(db, todo, todo_in)


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["todos"])
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    await crud.delete_todo(db, todo)
