from fastapi import FastAPI, HTTPException, Depends
from db import get_async_session
from models import Todo, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import shutil
import os
import uuid
import uvicorn
from todo.schemas import TodoCreate
 

app = FastAPI()

@app.get("/uploads")
async def show_todo(session: AsyncSession = Depends(get_async_session)) -> dict:
    
    result = await session.execute(select(Todo).order_by(Todo.updated_at.desc()))

    todos = [row[0] for row in result.all()]

    todo_data = []

    for todo in todos:
        todo_data.append(
            {
                "id":str(todo.id),
                "user_id": str(todo.user_id),
                "caption":todo.title,
                "description":todo.description,
                "completed": todo.completed,
                "created_at": todo.created_at,
                "updated_at": todo.updated_at
            }
        )


    return {"todos":todo_data}

@app.post("/uploads/")
async def create_todo(data: TodoCreate,user: User = Depends(current_active_user), session: AsyncSession = Depends(get_async_session)) -> dict:

    todo = Todo(
        id = uuid.uuid4(),
        user_id = user.id,
        title = data.title,
        description = data.description,
        completed = data.completed
    )

    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    return {"message":"Created Successful", "id": str(todo.id)}


@app.delete("/uploads/{id}")
async def delete_todo(id: uuid.UUID, user: User = Depends(current_active_user), session: AsyncSession = Depends(get_async_session)) -> dict:

    try:

        result = await session.execute(select(Todo).where(Todo.id == id))

        todo = result.scalar_one_or_none()

        if todo is None:
            raise HTTPException(status_code=404, detail="Item not found")

        if todo.user_id != user.id:
            raise HTTPException(status_code=403, detail="You dont have permission to delete")

        await session.delete(todo)
        await session.commit()

        return {"message": "Deleted Successful", "ID": "{id}"}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

    

@app.put("/uploads/{id}")
async def update_todo(id: uuid.UUID, data: TodoUpdate, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)) -> dict:

    result = await session(select(Todo).where(Todo.id == id))
    todo = result.scalar_one_or_none()

    if todo is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if Todo.id != id:
        raise HTTPException(status_code=403, detail="You have no permission to delete this")

    todo.title = data.title
    todo.description = data.description
    todo.completed = data.completed


    await session.commit()
    await session.refresh(todo)

    return {"message":"Updated Successful", "ID": str(todo.id)}




#=========================
#Testing
@app.get("/show")
def show_posts() -> dict:
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run("todo.app:app", host="0.0.0.0", port=8000, reload=True)