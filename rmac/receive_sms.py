################################################################################
# Simple(st) example for receiving notifications.
################################################################################
import aamnotifs as notifs
import logging
import atom
import gdata.contacts.data
import gdata.contacts.client
import getpass
from pync import Notifier
logging.basicConfig()
logging.getLogger('pika').setLevel(logging.INFO)

cache = {}
gd_client = None
def get_contact_name(number):
    if cache.get(number, None): #it's already in the cache so we won't hit the API again.
        return cache.get(number)
    contact = number #default cache value for each key
    query = gdata.contacts.client.ContactsQuery()
    query.text_query = number
    feed = gd_client.GetContacts(q=query)
    for i, entry in enumerate(feed.entry):
        contact = entry.title.text
    cache[number] = contact #update the cache
    return contact

def print_all_notifications(title, message):
    Notifier.remove('SMS_ALERTS')
    print "Notification received: {0}: {1}".format(title, message)
    number = title.strip('Number::').strip('+1').strip('+27')
    try:
        contact = get_contact_name(number)
    except Exception as e:
        print e
    print 'This is the Contact: %s' % (contact)

    Notifier.notify(message.strip('Msg::'), title='TXT From: %s' % contact, group='SMS_ALERTS')



def print_mail_and_irc_notifications(title, message):
    print "Mail and IRC notifications received: {0}: {1}".format(title, message)

try:
    user = raw_input('Please enter your Google username: ')
    passwd = getpass.getpass()
    gd_client = gdata.contacts.client.ContactsClient(source='GoogleInc-ContactsPythonSample-1')
    gd_client.ClientLogin(user, passwd, gd_client.source)
    n = notifs.Notifs("amqp://adewinter:qsczse12@base102.net:5672/%2F")

    # The routing_name is the name of the "channel" you want to use
    # it can be "mail", "chat", etc.
    # This will make it easy to choose which channels your clients
    # will receive. Can be a list too, for listening on multiple streams.
    n.receive("sms_notification", print_all_notifications)  # "#" matches all channels

    # OR n.receive(["mail", "irc"], print_mail_and_irc_notifications)

except KeyboardInterrupt:
    pass
