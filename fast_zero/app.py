from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
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
