from http import HTTPStatus
from random import choice, randint

from sqlalchemy import select

from fast_zero.models import Todo, TodoState, User
from tests.factories import TodoModelFactory, TodoSchemaFactory


def test_relationship_user_todos(session, user: User):
    todo = TodoModelFactory(user_id=user.id)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user_db = session.scalar(select(User).where(User.id == user.id))

    assert todo in user_db.todos


def test_relationship_todos_user(session, user: User):
    todo = TodoModelFactory(user_id=user.id)

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

    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()
    assert 'id' in response_data
    assert 'created_at' in response_data
    assert 'updated_at' in response_data

    for key in todo:
        assert response_data[key] == todo[key]


def test_list_todos__fields_shoul_be_equal(session, client, user, token):
    todo = TodoModelFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    todo_db = response.json()['todos'][0]

    assert 'id' in todo_db
    assert todo_db['title'] == todo.title
    assert todo_db['description'] == todo.description
    assert todo_db['state'] == todo.state.value
    assert todo_db['created_at'] == todo.created_at.isoformat()
    assert todo_db['updated_at'] == todo.updated_at.isoformat()


def test_list_todos(session, client, user, token):
    todos = randint(0, 50)
    session.bulk_save_objects(
        TodoModelFactory.create_batch(todos, user_id=user.id)
    )
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
    session.bulk_save_objects(
        TodoModelFactory.create_batch(todos, user_id=user.id)
    )
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
        TodoModelFactory.create_batch(
            todos, user_id=user.id, title='Test todo 1'
        )
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
        TodoModelFactory.create_batch(
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
        TodoModelFactory.create_batch(todos, user_id=user.id, state=state)
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
        TodoModelFactory.create_batch(
            todos,
            user_id=user.id,
            title=title,
            description=description,
            state=state,
        )
    )

    session.bulk_save_objects(
        TodoModelFactory.create_batch(
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
    todo = TodoModelFactory(user_id=user.id)

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


def test_delete_todo_not_found(client, token):
    todo_id = 1e9
    response = client.delete(
        f'/todos/{todo_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_delete_todo_successfully(client, session, user, token):
    todo = TodoModelFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'Task deleted successfully.'
