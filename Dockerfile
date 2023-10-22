FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]