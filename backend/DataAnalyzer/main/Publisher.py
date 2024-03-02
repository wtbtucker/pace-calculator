import pika

class Publisher:
    def __init__(self):
        # TCP internal address for broker hosted on Render
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-1wih:4369'))
        self.channel = connection.channel
        self.channel.queue_declare(queue='zipcode')
    
    def send_zipcode(self, zipcode):
        self.channel.basic_publish(exchange='',
                      routing_key='zipcode',
                      body='02155')
        print("[x] Sent 02155")