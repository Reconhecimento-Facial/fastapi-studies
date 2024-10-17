from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy import select

from fast_zero.models import Todo
from fast_zero.schemas import (
    FilterTodoSchema,
    TodoListSchema,
    TodoPublicSchema,
    TodoSchema,
)
from fast_zero.type import T_CurrentUser, T_Session

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=TodoPublicSchema,
)
def create_todo(
    todo: TodoSchema,
    current_user: T_CurrentUser,
    session: T_Session,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=current_user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoListSchema)
def todos_list(
    session: T_Session,
    current_user: T_CurrentUser,
    todo_filter: FilterTodoSchema = Depends(),
):
    query = select(Todo).where(Todo.user_id == current_user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if todo_filter.description:
        query = query.filter(
            Todo.description.contains(todo_filter.description)
        )

    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = session.scalars(
        query.offset(todo_filter.offset).limit(todo_filter.limit)
    ).all()

    return {'todos': todos}
