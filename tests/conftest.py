from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


@pytest.fixture
def user(session: Session) -> User:
    user = User(username='Teste', email='teste@test.com', password='testtest')

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def client(session: Session) -> Generator[TestClient, None, None]:
    def get_session_teste():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_teste
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session() -> Generator[Session, None, None]:
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
