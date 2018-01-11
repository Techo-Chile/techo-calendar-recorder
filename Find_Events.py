
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

class Find_Events():

	def __init__(self):
		try:
			import argparse
			self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
		except ImportError:
			self.flags = None
		#setea las flags
		self.SCOPES = 'https://www.googleapis.com/auth/calendar'
		#setea el scope, para la api de google calendar hay 2 scopes: aqui se utiliza
		#el scope que se utiliza aqui permite ver y editar eventos
		self.CLIENT_SECRET_FILE = 'client_secret.json'
		#setea la llave para acceder a la api desde la cuenta pyt (se encuentra en la carpeta)
		self.APPLICATION_NAME = 'Google Calendar API Python Quickstart'
		#setea el nombre de la aplicacion
		self.credentials = None
		self.service = None

	def set_credentials(self):
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		#sete el directorio de las credenciales
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		#si no existe, crea el directorio de las credenciales
		credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')
		store = Storage(credential_path)
		self.credentials = store.get()
		#consigue las credenciales
		if not self.credentials or self.credentials.invalid:
			flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
			flow.user_agent = self.APPLICATION_NAME
			if self.flags:
				self.credentials = tools.run_flow(flow, store, self.flags)
			else: # Needed only for compatibility with Python 2.6
				self.credentials = tools.run(flow, store)
			print('Storing credentials to ' + credential_path)
		#si no se encuentran las credenciales, las crea.
		http = self.credentials.authorize(httplib2.Http())
		self.service = discovery.build('calendar', 'v3', http=http)
		#accede a la api

	def get_events(self,calendar_id, initial_time, final_time):
		events_result = self.service.events().list(
			calendarId=calendar_id, timeMin=initial_time, timeMax=final_time,
			singleEvents=True, orderBy='startTime').execute()
		#busca los eventos de un tereminado calendario, entre un determinado periodo de tiempo
		#los ordena por tiempo de inicio
		return events_result.get('items',[])

	def get_event(self, calendar_id, event_id):
		return self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()
		#consigue un determinado evento de un determinado calendario

	def delete_event(self, calendar_id, event_id):
		return self.service.events().delete(calendarId = calendar_id, eventId = event_id).execute()
		#elimina un determinado evento de un determinado calendario


