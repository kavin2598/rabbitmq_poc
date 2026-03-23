import os
import time

import pika


def env(name: str, default: str) -> str:
    value = os.getenv(name)
    return value if value is not None and value != "" else default


def connection_parameters() -> pika.ConnectionParameters:
    host = env("RABBITMQ_HOST", "localhost")
    port = int(env("RABBITMQ_PORT", "5672"))
    user = env("RABBITMQ_USER", "guest")
    password = env("RABBITMQ_PASS", "guest")

    credentials = pika.PlainCredentials(user, password)
    return pika.ConnectionParameters(host=host, port=port, credentials=credentials)


def main() -> None:
    queue = env("RABBITMQ_QUEUE", "demo_queue")

    connection = pika.BlockingConnection(connection_parameters())
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    for i in range(1, 6):
        message = f"message-{i}"
        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(f"[producer] sent: {message}")
        time.sleep(1)

    connection.close()


if __name__ == "__main__":
    main()
