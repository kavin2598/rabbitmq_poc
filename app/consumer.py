import os

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

    def callback(ch: pika.adapters.blocking_connection.BlockingChannel, method, properties, body) -> None:
        message = body.decode()
        print(f"[consumer] received: {message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    print("[consumer] waiting for messages. press CTRL+C to stop.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[consumer] stopping...")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
