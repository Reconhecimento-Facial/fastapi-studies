from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='vinicabral', password='123', email='vinicius@exemplo.com'
    )

    session.add(user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'vinicabral'))

    assert user.username == 'vinicabral'
    assert user.password == '123'
    assert user.email == 'vinicius@exemplo.com'
