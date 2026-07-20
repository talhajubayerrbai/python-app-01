from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate


async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Todo]:
    result = await db.execute(select(Todo).offset(skip).limit(limit))
    return list(result.scalars().all())


async def get_todo(db: AsyncSession, todo_id: int) -> Optional[Todo]:
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    return result.scalar_one_or_none()


async def create_todo(db: AsyncSession, todo_in: TodoCreate) -> Todo:
    todo = Todo(
        title=todo_in.title,
        description=todo_in.description,
        completed=todo_in.completed,
    )
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_todo(
    db: AsyncSession, todo: Todo, todo_in: TodoUpdate
) -> Todo:
    update_data = todo_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    await db.commit()
    await db.refresh(todo)
    return todo


async def delete_todo(db: AsyncSession, todo: Todo) -> None:
    await db.delete(todo)
    await db.commit()
