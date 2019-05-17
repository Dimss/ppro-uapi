FROM python:3.7.3-alpine3.8
WORKDIR /app
RUN pip3.7 install pipenv
ADD uapi /app/hfdot
ADD Pipfile /app
ADD Pipfile.lock /app
RUN pipenv install
CMD pipenv run api