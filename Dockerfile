FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
CMD ["poetry", "run", "fastapi", "run", "fast_zero/app.py"]
