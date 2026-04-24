import pika

credentials = pika.PlainCredentials('student', 'student00')
parameters =  pika.ConnectionParameters('149.62.71.186', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

queue_name = 'JSON1'

def callback(ch, method, properties, body):
    print("Z binding %r smo prejeli sporočilo %r" % (method.routing_key, body.decode()))


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()