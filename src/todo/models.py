from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime 
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from uuid import UUID
from sqlalchemy import ForeignKey
import uuid

"""
Why we have base
====================
Base--
     |
     |- Todo
     |- User
====================
"""

#Base
class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    completed: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    user = relationship("User", back_populates="todos")


class User(SQLAlchemyBaseUserTableUUID, Base):
    todos = relationship("Todo", back_populates="user")