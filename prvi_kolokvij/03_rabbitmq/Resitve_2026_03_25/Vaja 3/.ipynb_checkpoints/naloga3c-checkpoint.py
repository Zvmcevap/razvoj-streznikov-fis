import pika

credentials = pika.PlainCredentials('student', 'student00')
parameters =  pika.ConnectionParameters('149.62.71.186', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='my_new_topic', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

def callback(ch, method, properties, body):
    if method.routing_key[:4] == 'big.':
        channel.basic_publish(exchange='topic_logs', routing_key='resend', body=body)
        print('Key binding je bil big.*.*, zato imamo resend')
    print("Z binding %r smo prejeli sporočilo %r" % (method.routing_key, body.decode()))

channel.queue_bind(exchange='my_new_topic', queue=queue_name, routing_key='*.*.fox')

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Consuming')
channel.start_consuming()