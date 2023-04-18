FROM python:3.8

RUN pip install poetry
COPY . /app
WORKDIR /app

RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi

ENV PYTHONPATH=$PWD:$PYTHONPATH

ENTRYPOINT ["python", "slsim"]
