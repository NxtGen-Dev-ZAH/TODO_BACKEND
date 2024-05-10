from typing import Optional

from sqlmodel import Field, Integer, SQLModel


class User(SQLModel):
    # A class representing a user.
    # __tablename__ = "Users"
    id: Optional[int] = Field(Integer, primary_key=True, index=True)
    username: str
    hashed_password: str


class Todo(SQLModel, table=True):
    # A class representing a todo item.
    __tablename__ = "Todos"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str
    description: str
    completed: bool = False
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Todoupdate(SQLModel):
    # A class representing a todo item.
    title: str
    description: str
    completed: bool = False
