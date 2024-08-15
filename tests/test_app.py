from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_read_root_deve_retornar_ok_e_hello_world():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'bem vindo a raiz do seu servidor'}


def test_read_ola_da_web_deve_retornar_ok_e_ola_mundo():
    response = client.get('/ola_da_web')
    print(response.text)
    assert response.status_code == HTTPStatus.OK
    assert 'Olá Mundo!' in response.text
