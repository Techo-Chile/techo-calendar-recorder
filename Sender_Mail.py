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
		#setea el cope, se utiliza el scope para enviar correos
		self.CLIENT_SECRET_FILE = 'client_secret.json'
		#setea la llave para acceder a la api desde la cuenta pyt (se encuentra en la carpeta)
		self.APPLICATION_NAME = 'Gmail API Python Quickstart'
		try:
			import argparse
			self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
		except ImportError:
			self.flags = None
		#setea las flags

	def set_credentials(self):
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		#sete el directorio de las credenciales
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		#si no existe, crea el directorio de las credenciales
		credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')
		store = Storage(credential_path)
		self.credentials = store.get()
		#consigue las credenciales
		if not self.credentials or self.credentials.invalid:
			flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
			flow.user_agent = self.APPLICATION_NAME
			if self.flags:
				self.credentials = tools.run_flow(flow, store, self.flags)
			else:
				self.credentials = tools.run(flow, store)
			print('Storing credentials to ' + credential_path)
		#si no se encuentran las credenciales, las crea.
		http = self.credentials.authorize(httplib2.Http())
		self.service = discovery.build('gmail', 'v1', http=http)
		#accede a la api

	def create_message(self,sender, to, subject, message_text):
		message = MIMEText(message_text, 'html')
		#crea un MIMEText que le permite agregar elementos de html
		message['to'] = to
		message['from'] = sender
		message['subject'] = subject
		b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
		b64_string = b64_bytes.decode()
		#codifica el mensaje
		return {'raw': b64_string, 'payload':{'mimeType':'text/html'}}
		#retorna el mensaje codificado y comprimido

	def send_message(self,user_id, message):
		message = (self.service.users().messages().send(userId=user_id, body=message).execute())
		#envia el mensaje
		return message
