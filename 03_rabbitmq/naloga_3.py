import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel = connection.channel()

exchange = "ime_exchangea"  # zamenjaj z dejanskim imenom exchange-a

channel.exchange_declare(
    exchange=exchange,
    exchange_type="topic"
)

ime_priimek = 'BenoZupanc'
queue_name = f"{ime_priimek}_znam"

channel.queue_declare(queue=queue_name)

binding_keys = [
    "matematika.*.*",
    "biologija.deljenje.*",
    "*.*.ja_ne",
]

for key in binding_keys:
    channel.queue_bind(
        exchange=exchange,
        queue=queue_name,
        routing_key=key
    )

def callback(ch, method, properties, body):
    question = body.decode()

    print(f"Dobil vprašanje: {question}")
    print(f"Odgovarjam: {question}")

    ch.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=question
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue=queue_name,
    auto_ack=False,
    on_message_callback=callback
)

print("Čakam na vprašanja...")
channel.start_consuming()