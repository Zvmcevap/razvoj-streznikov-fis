import pika

credentials = pika.PlainCredentials('martin', 'martin00')
parameters =  pika.ConnectionParameters('149.62.71.186', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

message = "Oranžna"

channel.basic_publish(exchange='topic_logs', routing_key='karkoli.orange.sdfsdfdsf', body=message)

connection.close()