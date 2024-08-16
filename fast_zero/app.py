from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import (
    MessageSchema,
    UserDBSchema,
    UserPublicSchema,
    UserSchema,
)

app = FastAPI()

database = []


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
def create_user(user: UserSchema):
    user_with_it = UserDBSchema(id=len(database) + 1, **user.model_dump())

    database.append(user_with_it)
    return user_with_it
