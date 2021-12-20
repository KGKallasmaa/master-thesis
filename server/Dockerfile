FROM python:3.9.9-slim-buster

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt


WORKDIR /src
COPY src/ .

EXPOSE 5000

CMD ["python", "./app.py"]
