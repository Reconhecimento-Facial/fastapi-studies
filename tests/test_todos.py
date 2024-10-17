from http import HTTPStatus
from random import choice, randint

from sqlalchemy import select

from fast_zero.models import Todo, TodoState, User
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


def test_list_todos(session, client, user, token):
    todos = randint(0, 50)
    session.bulk_save_objects(TodoFactory.create_batch(todos, user_id=user.id))
    session.commit()

    response = client.get(
        f'/todos/?limit={todos}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == todos


def test_list_todos_pagination(session, user, client, token):
    offset = randint(0, 5)
    limit = randint(0, 10)
    todos = randint(0, 50)
    session.bulk_save_objects(TodoFactory.create_batch(todos, user_id=user.id))
    session.commit()

    expected_todos = todos - offset
    expected_todos = max(expected_todos, 0)
    expected_todos = min(limit, expected_todos)

    response = client.get(
        f'/todos/?offset={offset}&limit={limit}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_title(session, user, client, token):
    todos = randint(0, 50)
    session.bulk_save_objects(
        TodoFactory.create_batch(todos, user_id=user.id, title='Test todo 1')
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == todos


def test_list_todos_filter_description(session, user, client, token):
    todos = randint(0, 50)
    session.bulk_save_objects(
        TodoFactory.create_batch(
            todos, user_id=user.id, description='description'
        )
    )
    session.commit()

    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == todos


def test_list_todos_filter_state(session, user, client, token):
    todos = randint(0, 50)
    state = choice([state.value for state in TodoState])

    session.bulk_save_objects(
        TodoFactory.create_batch(todos, user_id=user.id, state=state)
    )
    session.commit()

    response = client.get(
        f'/todos/?state={state}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == todos


def test_list_todos_filter_combined(session, user, client, token):
    todos = randint(0, 50)
    title = 'Test todo combined'
    description = 'combined description'
    state = choice([state.value for state in TodoState])
    session.bulk_save_objects(
        TodoFactory.create_batch(
            todos,
            user_id=user.id,
            title=title,
            description=description,
            state=state,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            randint(0, 50),
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TodoState.todo,
        )
    )
    session.commit()

    response = client.get(
        f'/todos/?title={title}&description={description}&state={state}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == todos


def test_todos_update_patch_not_found(client, token):
    todo_id = 1e9
    response = client.patch(
        f'/todos/{todo_id}',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_todo_patch_title(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()
    title = f'novo {todo.title}'
    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': title},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == title
