from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from fast_zero.models import Todo
from fast_zero.schemas import (
    FilterTodoSchema,
    MessageSchema,
    TodoListSchema,
    TodoPublicSchema,
    TodoSchema,
    TodoUpdateSchema,
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


@router.patch('/{todo_id}', response_model=TodoPublicSchema)
def todo_update_patch(
    todo_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
    todo: TodoUpdateSchema,
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == current_user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=MessageSchema)
def delete_todo(
    todo_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    todo_db = session.scalar(
        select(Todo).where(Todo.user_id == current_user.id, Todo.id == todo_id)
    )
    if not todo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(todo_db)
    session.commit()

    return {'message': 'Task deleted successfully.'}
