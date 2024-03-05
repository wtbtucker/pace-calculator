import pika


# class Credentials:
#     def __init__(self, username: str=None, password: str=None, erlang_cookie: str=None):
#         self.USERNAME = username
#         self.PASSWORD = password
#         self.COOKIE = erlang_cookie
    
#     def read_from_env(self):
#         load_dotenv()
#         self.USERNAME = os.getenv('RABBITMQ-USERNAME')
#         self.PASSWORD = os.getenv('RABBITMQ_PASSWORD')
#         self.COOKIE = os.getenv('RABBITMQ_ERLANG_COOKIE')


class Publisher:
    def __init__(self):
        # HTTP  internal address for broker hosted on Render
        # RABBITMQ_URL = self._load_url()
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='amqp://rabbitmq:rabbitmq@rabbitmq-1wih:5672'))
        self.channel = connection.channel()

    # def _load_url(self):
    #     load_dotenv()
    #     return os.getenv('RABBITMQ_URL')
    
    def send_zipcode(self, zipcode):
        self.channel.queue_declare(queue='zipcode')
        self.channel.basic_publish(exchange='',
                      routing_key='zipcode',
                      body=zipcode)
        print("[x] Sent 02155")