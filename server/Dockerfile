FROM python:3.9.5-slim-buster
RUN apt-get update && apt-get -y install gcc

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt


WORKDIR /src
COPY src/ .

EXPOSE 5000

CMD ["python", "./app.py"]