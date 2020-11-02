FROM python:3.8.5

ENV POSTGRES_USER=admin \
    POSTGRES_PASSWORD=password

COPY app /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]