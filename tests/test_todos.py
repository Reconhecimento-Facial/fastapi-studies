from http import HTTPStatus

from sqlalchemy import select

from fast_zero.models import Todo, User
from tests.factories import TodoFactory, TodoSchemaFactory


def test_relationship_user_todos(session, user: User):
    todo_schema = TodoSchemaFactory()

    todo = Todo(
        title=todo_schema.title,
        description=todo_schema.description,
        state=todo_schema.state,
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user_db = session.scalar(select(User).where(User.id == user.id))

    assert todo in user_db.todos


def test_relationship_todos_user(session, user: User):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    todo_db = session.scalar(select(Todo).where(Todo.id == todo.id))

    assert todo_db.user == user


def test_create_todos(client, user, token):
    todo = TodoSchemaFactory().model_dump()

    response = client.post(
        '/todos/',
        json=todo,
        headers={'Authorization': f'Bearer {token}'},
    )

    todo['id'] = response.json()['id']
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == todo
