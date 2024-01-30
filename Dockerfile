FROM python:3.11 as python-base
RUN mkdir code
WORKDIR  /code
COPY ./pyproject.toml /code/pyproject.toml
RUN apt-get install libpq-dev
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
CMD ["python3", "/code/main.py"]
