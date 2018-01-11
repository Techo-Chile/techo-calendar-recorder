import cherrypy
from Find_Events import *

class Calendars(object):

	def __init__(self):
		self.finder = Find_Events()
		self.finder.set_credentials()


	@cherrypy.expose
	def index(self):
		return "gestiones del calendario de techo"

	@cherrypy.expose
	@cherrypy.config(**{'response.stream': True})
	def delete_event(self, id_calendar, id_event):
		try:
			self.finder.delete_event(id_calendar)
			return "Sala liberada del evento"
		except:
			yield "error al borrar evento: <br>"
			yield "id "+id_event
			yield "<br>calendario "+id_calendar




if __name__ == '__main__':
	cherrypy.config.update({'server.socket_host': '0.0.0.0',})
	cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
	cherrypy.quickstart(Calendars())