import pika
import logging
logging.basicConfig()
logging.getLogger('pika').setLevel(logging.INFO)

logger = logging.getLogger('rmac')
logger.setLevel(logging.DEBUG)

class rmac(object):
    exchange = "rmac"
    url = "amqp://adewinter:qsczse12@base102.net:5672/%2F"
    e_type = "fanout"

    def __init__(self):
        try:
            logger.debug('Establishing Blocking Connection at URL %s' % self.url)
            self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
            logger.debug('Creating Channel')
            self.channel = self.connection.channel()
            logger.debug('Channel: %s' % self.channel)
            logger.debug('Declaring Exchange: %s. Type: %s' % (self.exchange, self.e_type))
            self.channel.exchange_declare(exchange=self.exchange, type=self.e_type)
        except:
            logger.error("Connection error! Couldn't establish connection to %s" % self.url)

    def consume(self):
        for method_frame, properties, body in self.channel.consume('test'):
            # Display the message parts and ack the message
            logger.debug('%s, %s, %s' % (method_frame, properties, body))
            self.channel.basic_ack(method_frame.delivery_tag)

            # Escape out of the loop after 10 messages
            if method_frame.delivery_tag == 10:
                logger.debug('Escaping from loop after 10 messages')
                break


    def receive(self, routings, callback):
        if type(routings) == str:
            routings = [routings]

        def internal_callback(ch, method, properties, body):
            logger.debug('Internal Callback: %s, %s, %s, %s' % (ch, method, properties, body))
            body = json.loads(body)
            callback(body["title"], body["message"])

        try:
            result = self.channel.queue_declare(exclusive=True)
            self.queue_name = result.method.queue

            for routing in routings:
                self.channel.queue_bind(exchange=self.exchange,
                                        queue=self.queue_name,
                                        routing_key=routing)
            self.channel.basic_consume(internal_callback, queue=self.queue_name,
                                       no_ack=True)
            self.channel.start_consuming()

        except:
            logger.debug('Receive exception issue!')
            time.sleep(2)
            # self.connect()
            self.receive(routings, callback)



logger.debug('Creating an rmac...')
r = rmac()
# r.consume()