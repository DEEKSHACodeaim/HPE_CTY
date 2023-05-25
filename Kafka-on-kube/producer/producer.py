from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import faker
from datetime import datetime
import logging
import time
from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

class Producer:

    def __init__(self):
        self._init_kafka_producer()

    def _init_kafka_producer(self):
        self.kafka_host = "kafka-local.default.svc.cluster.local:9092"
        self.kafka_topic = "my-topic"
        self.producer = KafkaProducer(

            bootstrap_servers=self.kafka_host, value_serializer=lambda v: json.dumps(v).encode(),

        )
    def publish_to_kafka(self, message):
        try:
            self.producer.send(self.kafka_topic, message)
            self.producer.flush()

        except KafkaError as ex:

            logging.error(f"Exception {ex}")
        else:
            logging.info(f"Published message {message} into topic {self.kafka_topic}")

    @staticmethod
    def create_random_email():
        f = faker.Faker()

        new_contact = dict(
            username=f.user_name(),
            first_name=f.first_name(),
            last_name=f.last_name(),
            email=f.email(),
            date_created=str(datetime.utcnow()),
        )

        return new_contact

producer = Producer()

@app.route('/producer',methods=['POST'])
def produce_message():
    data = request.get_json()
    message = data['message']
    response = {
        'status': 'success',
        'message': f'Received message: {message}'
    }
    producer.publish_to_kafka(message)
    return 'Message produced successfully'


@app.route('/',methods=['GET'])
def trial():
    return "Conection works!"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
    # print("Working till here")
