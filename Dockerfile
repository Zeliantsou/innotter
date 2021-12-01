FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY Pipfile.lock /code/
COPY Pipfile /code/

RUN pip install --upgrade pip

RUN apt install libpq-dev python-dev

RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile

COPY . /code/

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]