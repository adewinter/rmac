################################################################################
# Simple(st) example for sending a notification.
################################################################################
import aamnotifs
import logging
import argparse
logging.basicConfig()
logging.getLogger('pika').setLevel(logging.INFO)



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Send an SMS message')
	parser.add_argument('number', action='store')
	args = parser.parse_args()
	number = args.number
	message = raw_input('Please enter message to send: ')
	print 'Connecting to message queue...'
	n = aamnotifs.Notifs("amqp://adewinter:qsczse12@base102.net:5672/%2F")
	print 'Connected.\n'
	print 'Attempting to send message: %s :: to: %s' % (message, number)
	n.send("sms_notification", number, message)
	print 'Message sent.'
else:
	# The routing_name is the name of the "channel" you want to use
	# it can be "mail", "chat", etc.
	# This will make it easy to choose which channels your clients
	# will receive
	print 'Connecting to message queue...'
	n = aamnotifs.Notifs("amqp://adewinter:qsczse12@base102.net:5672/%2F")
	print 'Connected.\n'
	n.send("sms_send", "6176920786", "Foo!")
	n.connection.close()