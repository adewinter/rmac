from datetime import datetime
from pony.orm import *

db = Database("sqlite", "database2.sqlite", create_db=True)

class sms_received(db.Entity):
    sender = Required(str)
    message = Optional(str)
    timestamp = Required(datetime, default=datetime.now)
    replies = Set("sms_sent")
    archived = Required(bool, default=False)

class sms_sent(db.Entity):
    to = Required(str)
    message = Optional(str)
    timestamp = Required(datetime, default=datetime.now)
    reply_to = Optional(sms_received)
    archived = Required(bool, default=False)

sql_debug(True)
db.generate_mapping(create_tables=True)
# db.generate_mapping(check_tables=True)