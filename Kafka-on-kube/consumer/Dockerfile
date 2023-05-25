FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE=1

RUN pip3 install kafka-python
RUN pip3 install psycopg2-binary

COPY consumer.py .

CMD ["python3", "-u", "./consumer.py"]