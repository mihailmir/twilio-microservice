FROM python:3.11 as python-base
RUN mkdir code
WORKDIR  /code
COPY ./pyproject.toml /code/pyproject.toml
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0"
CMD ["python3", "/code/main.py", "--bind", "0.0.0.0:7000"]
