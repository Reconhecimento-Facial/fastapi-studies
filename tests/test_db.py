from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='Teste',
        email='teste@test.com',
        password='testtest',
    )
    session.add(user)
    session.commit()

    assert user.email == 'teste@test.com'
    assert user.password == 'testtest'
    assert user.username == 'Teste'
