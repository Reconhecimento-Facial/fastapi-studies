from http import HTTPStatus

from fast_zero.schemas import UserPublicSchema
from tests.factories import UserSchemaFactory


def test_create_user(client):
    user_schema = vars(UserSchemaFactory())

    response = client.post(
        '/users/',
        json=user_schema,
    )

    assert response.status_code == HTTPStatus.CREATED
    user_db = response.json()

    assert 'id' in user_db
    assert 'created_at' in user_db
    assert 'updated_at' in user_db
    assert user_db['username'] == user_schema['username']
    assert user_db['email'] == user_schema['email']


def test_create_user_username_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': f'{user.username}',
            'email': 'teste_email_diferente@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste_username_diferente',
            'email': f'{user.email}',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_create_user_username_and_email_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': f'{user.username}',
            'email': f'{user.email}',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username and email already exists'}


def test_read_users_with_users(client, user):
    user_public = UserPublicSchema.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    user_public['created_at'] = user_public['created_at'].isoformat()
    user_public['updated_at'] = user_public['updated_at'].isoformat()
    assert response.json() == {'users': [user_public]}


def test_get_user(client, user):
    user_public = UserPublicSchema.model_validate(user).model_dump()
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    user_public['created_at'] = user_public['created_at'].isoformat()
    user_public['updated_at'] = user_public['updated_at'].isoformat()
    assert response.json() == user_public


def test_get_user_not_found(client, user):
    response = client.get(f'/users/{user.id + 1}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    user_schema = vars(UserSchemaFactory())
    response = client.put(
        f'/users/{user.id}',
        json=user_schema,
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    user_db = response.json()

    assert 'id' in user_db
    assert 'created_at' in user_db
    assert 'updated_at' in user_db
    assert user_db['username'] == user_schema['username']
    assert user_db['email'] == user_schema['email']


def test_update_user_forbidden(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
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


def test_delete_user_forbidden(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
