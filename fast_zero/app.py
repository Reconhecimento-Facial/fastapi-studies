from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, users
from fast_zero.schemas import MessageSchema

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def read_root():
    return {'message': 'bem vindo a raiz da sua aplicação'}


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
