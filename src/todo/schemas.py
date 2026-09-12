from pydantic import BaseModel

class CreateTodo():
    title: str
    description: str
    completed: bool = False