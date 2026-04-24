import pika

credentials = pika.PlainCredentials('student', 'student00')
parameters =  pika.ConnectionParameters('149.62.71.186', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

message = "Vsebina poslanega sporočila"

channel.basic_publish(exchange='topic_logs_fox', routing_key='small.orange.fox', body=message)
channel.basic_publish(exchange='topic_logs', routing_key='big.orange.fox', body=message)
channel.basic_publish(exchange='topic_logs', routing_key='small.brown.fox', body=message)
channel.basic_publish(exchange='topic_logs', routing_key='big.brown.fox', body=message)
channel.basic_publish(exchange='topic_logs', routing_key='small.orange.bear', body=message)
channel.basic_publish(exchange='topic_logs', routing_key='big.orange.bear', body=message)
channel.basic_publish(exchange='topic_logs', routing_key='small.brown.bear', body=message)
channel.basic_publish(exchange='topic_logs', routing_key='big.brown.bear', body=message)


connection.close()
