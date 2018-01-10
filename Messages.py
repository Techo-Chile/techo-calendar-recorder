import dates
import random

def random_face():
	faces = {0:"o.O", 1:":)", 2:":D", 3:":P", 4: "(:", 5: "\ (•◡•) /", 6:"ʕ•ᴥ•ʔ", 7:'(¬‿¬)',
		8:'♥‿♥', 9:'( ͡ᵔ ͜ʖ ͡ᵔ )', 10:'◉_◉' }

	return faces[int(random.randrange(0,6,1))]

def add0(number):
	if number == '0':
		return '00'
	else:
		return number

def create_message(event_place, event_owner):
	initial_date = dates.get_uct_date(event_place['start']['dateTime'])
	final_date = dates.get_uct_date(event_place['end']['dateTime'])

	name_event = event_place['summary']

	try:
		name_creator = event_place['creator']['displayName']
	except:
		name_creator = ''

	
	mail_creator = event_place['creator']['email']

	link_place = event_place['htmlLink']
	link_owner = event_owner['htmlLink']


	try:
		place = event_place['location']
		if '@' in place:
			raise
	except:
		for value in event_place['attendees']:
			if 'resource' in value:
				place = value['displayName']

	ans = "<h3>Hola "+name_creator+"</h3>"
	ans += "Tiene un evento llamado "
	ans += "<b>"+name_event+"</b>"
	ans += " agendado para el dia "
	ans += "<b>"+str(initial_date.day)+" de "+dates.get_month(initial_date.month)+" </b>"
	ans += "entre las horas "
	ans += "<b>"+str(initial_date.hour)+":"+add0(str(initial_date.minute))+"</b> y "
	ans += "<b>"+str(final_date.hour)+":"+add0(str(final_date.minute))+"</b>"
	ans += "<br><br>"
	ans += "Este evento utilizara la sala "
	ans += "<b>"+place+"</b>"
	ans += "<br><br>"
	ans += "En caso de que este evento no se realizara o cambiara de lugar, se le pide ingresar al siguiente "
	ans += "<b>  <a href="+link_owner+">link</a> </b> y realice los cambios oportunos"

	ans += "<br><br><br>"
	ans += "Muchas Gracias! PyT Techo "+random_face()
	return ans





