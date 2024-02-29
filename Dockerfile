FROM python:3.10

ENV POSTGRES_DB_URL=postgresql://postgres:AwesomeGod003@172.17.0.3:5432/fastapi-docker-demo

WORKDIR /app 

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN alembic stamp head

RUN alembic upgrade head

EXPOSE 8000 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]