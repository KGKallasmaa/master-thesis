FROM python:3.10-slim-buster

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt


WORKDIR /src
COPY src/ .

CMD ["python", "./app.py"]
