from http import HTTPStatus

from tests.factories import TodoSchemaFactory


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
