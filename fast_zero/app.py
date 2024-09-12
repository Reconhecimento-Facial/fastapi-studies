from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    MessageSchema,
    UserPublicSchema,
    UserSchema,
    UsersListSchema,
)

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def read_root():
    return {'message': 'bem vindo a raiz do seu servidor'}


@app.get('/ola_da_web', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_ola_da_web():
    return """
    <html>
        <head>
            <title>Olá Mundo da Web!</title>
        </head>
        <body>
            <h1>Olá Mundo!</h1>
        </body>
    </html>
    """


@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if (db_user.username == user.username and db_user.email == user.email):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username and email already exists',
            )
        elif db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def get_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UsersListSchema)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    session.delete(db_user)
    session.commit()
    return {'message': 'User deleted successfully'}
