FROM python:3.11-slim

RUN pip install poetry==1.6.1

RUN poetry config virtualenvs.create false

WORKDIR /code

COPY ./pyproject.toml ./README.md ./poetry.lock* ./

RUN poetry install  --no-interaction --no-ansi --no-root

COPY ./client ./client

EXPOSE 8080

CMD streamlit run client/app.py
