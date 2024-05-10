from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, Field, SQLModel, create_engine, select
from todo_backend import models
from contextlib import asynccontextmanager
from todo_backend import database

connection_string = str(database.SECRET_KEY).replace("postgresql", "postgresql+psycopg")
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


@app.post("/create", response_model=models.Todo)
async def create_todo(
    requestt: models.Todo, session: Annotated[Session, Depends(get_session)]
):
    # with Session(engine) as session:
    todo = models.Todo(
        title=requestt.title,
        description=requestt.description,
        completed=requestt.completed,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.get("/todo")
async def get_all_todos(session: Annotated[Session, Depends(get_session)]):

    todos_query = session.exec(select(models.Todo)).all()
    return todos_query


@app.get("/todo/{todo_id}")
async def get_todos_by_id(
    todo_id: int, session: Annotated[Session, Depends(get_session)]
):
    todos = session.exec(select(models.Todo).where(models.Todo.id == todo_id)).first()
    return todos

    # todos_query = session.get(models.Todo, todo_id)
    # return todos_query


# @app.get("/done")
# def list_done_todos():
#     with Session() as sess:
#     todos_query = sess.(models.Todo)
#     done_todos_query = todos_query.filter(models.Todo.completed == True)
#     return done_todos_query.all()


@app.patch("/update/{id}")
async def update_todo(id: int, update:models.Todoupdate,session: Annotated[Session, Depends(get_session)]):

    try:
        todo_query = session.get( models.Todo , id)# whole model class will be equal to id of todo to update

        if not todo_query:
            raise HTTPException(status_code=404, detail="Blog not found")

        if update.title is not None:
            todo_query.title = update.title

        if update.description is not None:
            todo_query.description = update.description

        if update.completed is not None:
            todo_query.completed = update.completed

        session.add(todo_query)
        session.commit()
        session.refresh(todo_query)
        return {"todo updated": id}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()


@app.delete("/delete/{id}")
async def delete_todo(id: int, session: Annotated[Session, Depends(get_session)]):

    try:
        todo_query = session.get(models.Todo, id)
        if not todo_query:
            return {"message": "Todo not found"}

        session.delete(todo_query)
        session.commit()
        return {"todo deleted": id}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()
