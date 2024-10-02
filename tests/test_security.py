from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token
from fast_zero.settings import Settings

settings = Settings()


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert decoded['exp']


def test_get_current_user_invalid_token(client, user):
    response = client.delete(
        f'/users/{user.id}',
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


def test_get_current_user_user_not_exist(client, user):
    token_of_non_existing_user = create_access_token(
        data={'sub': 'doesntexist@doesntexist.com'}
    )
    response = client.delete(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token_of_non_existing_user}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
