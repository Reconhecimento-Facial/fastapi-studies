from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_hello_world(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'bem vindo a raiz do seu servidor'}


def test_read_ola_da_web_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/ola_da_web')
    print(response.text)
    assert response.status_code == HTTPStatus.OK
    assert 'Olá Mundo!' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'lucas',
            'email': 'lucas@exemplo.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'lucas',
        'email': 'lucas@exemplo.com',
    }
