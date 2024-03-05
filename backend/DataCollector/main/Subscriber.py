import pika

class Subscriber:
    def __init__(self) -> None:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.channel = connection.channel()
        
    
    def _callback(self, ch, method, properties, body):
        print(f" [x] Received {body}")

    def listen_for_zipcode(self, callback=_callback):
        self.channel.queue_declare(queue='zipcode')
        self.channel.basic_consume(queue='zipcode',
                                   auto_ack=True,
                                   on_message_callback=callback)
        self.channel.start_consuming()
        
