from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session, user):
    session.add(user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'Teste'))

    assert user.email == 'teste@test.com'
    assert user.password == 'testtest'
    assert user.username == 'Teste'
