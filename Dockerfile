FROM python:3.6

RUN mkdir /neo4j && /gnbr 

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

