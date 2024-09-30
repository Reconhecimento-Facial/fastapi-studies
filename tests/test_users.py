from http import HTTPStatus

from fast_zero.schemas import UserPublicSchema


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'username-de-teste',
            'email': 'email-de-teste@exemplo.com',
            'password': 'senha-de-teste',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'username-de-teste',
        'email': 'email-de-teste@exemplo.com',
    }


def test_create_username_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'teste_email_diferente@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_email_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste_username_diferente',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_create_username_and_email_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username and email already exists'}


def test_read_users_with_users(client, user):
    user_public = UserPublicSchema.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_public]}


def test_get_user(client, user):
    user_public = UserPublicSchema.model_validate(user).model_dump()
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_public


def test_get_user_not_found(client, user):
    response = client.get(f'/users/{user.id + 1}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'teste_com_put',
            'email': 'teste_put@put.com',
            'password': 'teste_senha_put',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'teste_com_put',
        'email': 'teste_put@put.com',
    }


def test_update_user_forbidden(client, user, token):
    response = client.put(
        f'/users/{user.id + 1}',
        json={
            'username': 'teste_com_put',
            'email': 'teste_put@put.com',
            'password': 'teste_senha_put',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


def test_delete_user_forbidden(client, user, token):
    response = client.delete(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
