FROM python:3.9-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install -- deploy --ignore-pipfile

COPY . .

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]