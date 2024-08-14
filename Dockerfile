# syntax=docker/dockerfile:1

FROM python:3.12.5-slim-bookworm

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . . 

RUN python pop_db.py

CMD [ "flask", "run", "--host=0.0.0.0"]