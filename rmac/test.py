#!/Users/adewinter/venv/rmac/bin/python
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from send import send_message as send
from pony.orm import *
from models import sms_received, sms_sent

@db_session
def add_entry_to_sent(number, message):
	sms_sent(to=number, message=message)

def create_get_message_text(number, holder):
	def get_message_text(instance):
		text = TextInput(text=' ', multiline=False)
		def send_message(instance):
			print 'Text input text is: %s' % instance.text
			print 'Sending to number: %s' % number
			send(number, instance.text)
			add_entry_to_sent(number, instance.text)
		text.bind(on_text_validate=send_message)
		holder.add_widget(text)
	return get_message_text

def get_stored_messages():
	received = sms_received.select().order_by(desc(sms_received.timestamp))
	received.show()
	return received

def make_message_widget(sender, text):
	"""
	Builds a GridLayout with appropriate label texts and buttons for actions.
	"""
	print 'Making widget for %s:%s' % (sender, text)
	message = GridLayout(cols=1, size_hint_y=0.3)
	buttons = GridLayout(cols=2, size_hint=(1,0.4))
	reply_button = Button(text='Reply')
	reply_button.bind(on_press=create_get_message_text(sender, message))
	buttons.add_widget(reply_button)
	buttons.add_widget(Button(text='Archive'))
	header = Label(text='[b]Sender: %s[/b]' % sender,markup=True, font_size='20sp', size_hint=(1.0,0.3))
	body = Label(text=text, size_hint=(1.0, 0.3))
	message.add_widget(header)
	message.add_widget(body)
	message.add_widget(buttons)
	return message



class TestApp(App):
    @db_session
    def build(self):
		heading = Label(text='[color=ff3333]Message[/color][color=3333ff]Viewer[/color]',
    					markup=True, size_hint=(1.0, 0.10), height=50, font_size='20sp')
		message_list = GridLayout(cols=1,size_hint_y=None, spacing=10,row_default_height=140, height=800)
		message_list.bind(minimum_height=message_list.setter('height'))
		# message_list.add_widget(heading)
		# message_list.add_widget(heading)

		#I don't know why I have to do this.  It appears the ScrollView eats the first two widgets. So I add two dummy ones to offset
		#it's horrible practice but frankly I don't care enough to fix it for real.
		message_list.add_widget(make_message_widget('null', 'null'))
		message_list.add_widget(make_message_widget('null', 'null'))
		message_list.add_widget(heading)
		for message in get_stored_messages():
			m_widget = make_message_widget(message.sender, message.message)
			print 'Widget made: %s:: %sx%s' % (m_widget, m_widget.width, m_widget.height)
			message_list.add_widget(m_widget)

		scroll_message_list=ScrollView(size_hint=(None, None), size=(800, 900))
		scroll_message_list.add_widget(message_list)
		# message_list.add_widget(make_message_widget('6176920786', 'This is the text of the message'))
		
		# base.add_widget(scroll_message_list)
		return scroll_message_list

TestApp().run()