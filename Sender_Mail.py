from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from email.mime.text import MIMEText
import base64





class Sender_Mail():

	def __init__(self):
		self.credentials = None
		self.service = None
		self.SCOPES = 'https://www.googleapis.com/auth/gmail.send'
		self.CLIENT_SECRET_FILE = 'client_secret.json'
		self.APPLICATION_NAME = 'Gmail API Python Quickstart'
		try:
			import argparse
			self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
		except ImportError:
			self.flags = None

	def set_credentials(self):
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')
		store = Storage(credential_path)
		self.credentials = store.get()

		if not self.credentials or self.credentials.invalid:
			flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
			flow.user_agent = self.APPLICATION_NAME
			if self.flags:
				self.credentials = tools.run_flow(flow, store, self.flags)
			else:
				self.credentials = tools.run(flow, store)
			print('Storing credentials to ' + credential_path)

		http = self.credentials.authorize(httplib2.Http())
		self.service = discovery.build('gmail', 'v1', http=http)

	def create_message(self,sender, to, subject, message_text):
		message = MIMEText(message_text, 'html')
		message['to'] = to
		message['from'] = sender
		message['subject'] = subject
		b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
		b64_string = b64_bytes.decode()
		return {'raw': b64_string, 'payload':{'mimeType':'text/html'}}

	def send_message(self,user_id, message):
		message = (self.service.users().messages().send(userId=user_id, body=message).execute())
		#print( 'Message Id: %s' % message['id'])
		return message

#sender = Sender_Mail()
#sender.set_credentials()
#msg = sender.create_message('jorge <jorge.pinto@techo.org>', 'jorge.pinto@techo.org', "hola", "<h1>hola</h1>")
#sender.send_message('jorge.pinto@techo.org', msg)
