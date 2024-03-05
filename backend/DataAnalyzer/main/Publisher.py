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
        credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
        parameters = pika.ConnectionParameters(host='rabbitmq-1wih', port=5672, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
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