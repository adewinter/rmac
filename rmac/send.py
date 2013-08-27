#!/Users/adewinter/venv/mq/bin/python

################################################################################
# Simple(st) example for sending a notification.
################################################################################
import aamnotifs
import logging
import requests
import json


# logging.basicConfig()
# logging.getLogger('pika').setLevel(logging.INFO)
def send_message(number, message):
	# print 'Connecting to message queue...'
	# n = aamnotifs.Notifs("amqp://adewinter:qsczse12@base102.net:5672/%2F")
	# print 'Connected.\n'
	# print 'Attempting to send message: %s :: to: %s' % (message, number)
	# n.send("sms_send", number, message)
	# print 'Message sent.'
	# n.connection.close()
	url = 'https://base102.net/send/'
	payload = {
	    'message': message,
	    'number': number
	}

	r = requests.post(url, data=json.dumps(payload))


	requests.post('https://base102.net/')
	print 'Sent request to https://base102.net/send/'
	print 'Number: %s' % number
	print 'Message: %s' % message
	print 'Request stat: %s, request text: %s' % (r.status_code, r.text)


# if __name__ == "__main__":
# 	import argparse

# 	parser = argparse.ArgumentParser(description='Send an SMS message')
# 	parser.add_argument('number', action='store')
# 	parser.add_argument('message', action='store')
# 	args = parser.parse_args()
# 	number = args.number
# 	message = args.message
# 	print 'Connecting to message queue...'
# 	n = aamnotifs.Notifs("amqp://adewinter:qsczse12@base102.net:5672/%2F")
# 	print 'Connected.\n'
# 	send_message(number,message)
	
	
