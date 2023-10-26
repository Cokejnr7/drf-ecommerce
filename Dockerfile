FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]