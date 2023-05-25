from kafka import KafkaConsumer
import logging
import psycopg2

# PostgreSQL connection details
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'qTJdkXTfPk'
POSTGRES_HOST = 'postgres-db-postgresql.default.svc.cluster.local'
POSTGRES_PORT = '5432'
POSTGRES_DB = 'threadweaver'

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    database=POSTGRES_DB
)

logging.basicConfig(level=logging.INFO)


class Consumer:

    def __init__(self):
        self._init_kafka_consumer()

    def _init_kafka_consumer(self):
        self.kafka_host = "kafka-local.default.svc.cluster.local:9092"
        self.kafka_topic = "my-topic"
        self.consumer = KafkaConsumer(
            "my-topic",
            bootstrap_servers=self.kafka_host,
        )

    def consume_from_kafka(self):
        for message in self.consumer:

            cur = conn.cursor()
            # Define the insert statement
            insert_stmt = str(message.value,'UTF-8')
            return_stmt = insert_stmt[1:-1];
            logging.info(return_stmt)
            # Execute the insert statement with the values
            cur.execute(return_stmt)

            # Get the number of rows affected by the previous insert statement
            row_count = cur.rowcount

            # Commit the transaction
            conn.commit()

            # Close the cursor and database connection
            cur.close()
            # Check if the insert was successful
            if row_count == 1:
                logging.info("Insert was successful")
            else:
                logging.info("Insert failed")


if __name__ == "__main__":

    consumer = Consumer()
    while True:
        consumer.consume_from_kafka()
    conn.close()
