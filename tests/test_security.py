from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['test'] == data['test']
    assert decoded['exp']


def test_get_current_user_invalid_token(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer token-invalido'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_none_username(client, user):
    token_quebrado = create_access_token(data={'sub': None})

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token_quebrado}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_user_not_exist(client):
    token_of_non_existing_user = create_access_token(
        data={'sub': 'doesntexist@doesntexist.com'}
    )
    response = client.delete(
        '/users/666',
        headers={'Authorization': f'Bearer {token_of_non_existing_user}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
