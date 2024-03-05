import pika

class Subscriber:
    def __init__(self) -> None:
        credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
        parameters = pika.ConnectionParameters(host='rabbitmq-1wih', port=5672, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()
        
    
    def _callback(self, ch, method, properties, body):
        print(f" [x] Received {body}")

    def listen_for_zipcode(self, callback=_callback):
        self.channel.queue_declare(queue='zipcode')
        self.channel.basic_consume(queue='zipcode',
                                   auto_ack=True,
                                   on_message_callback=callback)
        print(' [*] Waiting for messages')
        self.channel.start_consuming()
        
