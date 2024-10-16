from http import HTTPStatus

from fastapi import APIRouter

from fast_zero.models import Todo, TodoState
from fast_zero.schemas import TodoPublicSchema, TodoSchema, TodoListSchema
from fast_zero.type import T_CurrentUser, T_Session

from sqlalchemy import select

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


@router.get(
    '/',
    response_model=TodoListSchema
)
def todos_list(
    session: T_Session,
    current_user: T_CurrentUser,
    title: str | None = None,
    description: str | None = None,
    state: TodoState | None = None,
    offset: int | None = None, 
    limit: int | None = None,
):
    query = select(Todo).where(Todo.user_id == current_user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(
            Todo.description.contains(description)
        )

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(
        query.offset(offset).limit(limit)
    ).all()

    return {'todos': todos}