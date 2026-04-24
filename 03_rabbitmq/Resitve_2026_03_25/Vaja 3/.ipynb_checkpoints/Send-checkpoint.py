#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pika

credentials = pika.PlainCredentials('martin', 'martin00')
parameters =  pika.ConnectionParameters('149.62.71.186', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

message = "Vsebina poslanega sporočila"

channel.basic_publish(exchange='my_new_topic', routing_key='small.fox.original', body=message)
channel.basic_publish(exchange='my_new_topic', routing_key='big.fox.original', body=message)
channel.basic_publish(exchange='my_new_topic', routing_key='small.cat.original', body=message)
channel.basic_publish(exchange='my_new_topic', routing_key='big.cat.original', body=message)


connection.close()


# In[ ]:




