
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
		self.SCOPES = 'https://www.googleapis.com/auth/calendar'
		self.CLIENT_SECRET_FILE = 'client_secret.json'
		self.APPLICATION_NAME = 'Google Calendar API Python Quickstart'
		self.credentials = None
		self.service = None

	def set_credentials(self):
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')
		store = Storage(credential_path)
		self.credentials = store.get()
		if not self.credentials or self.credentials.invalid:
			flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
			flow.user_agent = self.APPLICATION_NAME
			if self.flags:
				self.credentials = tools.run_flow(flow, store, self.flags)
			else: # Needed only for compatibility with Python 2.6
				self.credentials = tools.run(flow, store)
			print('Storing credentials to ' + credential_path)
		http = self.credentials.authorize(httplib2.Http())
		self.service = discovery.build('calendar', 'v3', http=http)

	def get_events(self,calendar_id, initial_time, final_time):
		events_result = self.service.events().list(
			calendarId=calendar_id, timeMin=initial_time, timeMax=final_time,
			singleEvents=True, orderBy='startTime').execute()
		return events_result.get('items',[])

	def get_event(self, calendar_id, event_id):
		return self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()

	def delete_event(self, calendar_id, event_id):
		return self.service.events().delete(calendarId = calendar_id, eventId = event_id).execute()


'''now = datetime.datetime.utcnow().isoformat() + 'Z'
tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)

tomorrow = tomorrow.isoformat()+'Z'
print(now)
print(tomorrow)
finder = Find_Events()
finder.set_credentials()
events = finder.get_events('techo.org_333634383939383839@resource.calendar.google.com',now,tomorrow)
for event in events:
	print(event)
print(finder.get_event('cesar.desouza@techo.org','2k116bnk6g6iop8l0trmnpk3am'))
'''