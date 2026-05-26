import pika
import time
import numpy as np

credentials = pika.PlainCredentials('martin', 'martin00')
parameters = pika.ConnectionParameters(
    '149.62.71.186', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Queue ostane živ tudi po restartu RabbitMQ (ampak zgolj metadata!)
result_vejice = channel.queue_declare(queue='', exclusive=True)
queue_name_vejice = result_vejice.method.queue
result_x = channel.queue_declare(queue='', exclusive=True)
queue_name_x = result_x.method.queue

# MQrabbit zagotovi, da bo sporočilo zapisano! ===> PERSISTENT, isto kot delivery_mode = 2
properties = pika.BasicProperties(
    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)

for i in range(10):
    body = f'{np.random.randint(1, 6)},{np.random.randint(1, 6)}'
    print(f"task {body} given away!")
    channel.basic_publish(
        exchange='', routing_key=queue_name_vejice, body=body, properties=properties)

# good worker

channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    i, j = body.decode().split(',')

    product = int(i) * int(j)
    result = f"{i}x{j}={product}"

    ch.basic_publish(
        exchange='',
        routing_key=queue_name_x,
        body=result
    )

    print(result)
    ch.basic_ack(delivery_tag=method.delivery_tag)


# badworker
def callback(ch, method, properties, body):
    msg = body.decode()
    i, j = msg.split(',')

    if i == '1' or j == '1':
        print(f"Worker 2 saw 1 in {msg}, rejecting...")
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True
        )
        time.sleep(0.5)
        return

    product = int(i) * int(j)
    result = f"{i}x{j}={product}"

    ch.basic_publish(
        exchange='',
        routing_key=queue_name_x,
        body=result
    )

    print(result)
    ch.basic_ack(delivery_tag=method.delivery_tag)
