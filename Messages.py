import dates
import random

def random_face():
	faces = {0:"o.O", 1:":)", 2:":D", 3:":P", 4: "(:", 5: "\ (•◡•) /", 6:"ʕ•ᴥ•ʔ", 7:'(¬‿¬)',
		8:'♥‿♥', 9:'( ͡ᵔ ͜ʖ ͡ᵔ )', 10:'◉_◉' }

	return faces[int(random.randrange(0,11,1))]
	#retorna una carita al azar


def add0(number):
	if number == '0':
		return '00'
	else:
		return number
	#metodo creado para cuando se castea 00 a string -> lo castea como 0

def create_message(event_place, event_owner, id_calendar):
	initial_date = dates.get_uct_date(event_place['start']['dateTime'])
	final_date = dates.get_uct_date(event_place['end']['dateTime'])
	#consigue la fecha inicial y final del evento y las transoforma en horario chileno

	try:
		name_event = event_place['summary']
	except KeyError:
		name_event = 'Sin título'
	#nombre del evento

	try:
		name_creator = event_place['creator']['displayName']
	except:
		name_creator = ''
	#consigue nombre del creador, en caso de que no posea nombre de gmail, lo deja en blanco

	
	mail_creator = event_place['creator']['email']
	#mail del creador

	link_place = event_place['htmlLink']
	link_owner = event_owner['htmlLink']
	#link del evento del recurso(lugar) y link del evento del creador


	try:
		place = event_place['location']
		if '@' in place:
			raise
	except:
		for value in event_place['attendees']:
			if 'resource' in value:
				place = value['displayName']
	#busca el nombre del lugar, en caso de que no se encuentre en la informacion del evento
	#lo busca en la lista de invitados (ya que ahi se encuentra siempre)

	ans = "<h3>Hola "+name_creator+"</h3>"
	ans += "Tienes un evento llamado "
	ans += "<b>"+name_event+"</b>"
	ans += " agendado para el día "
	ans += "<b>"+str(initial_date.day)+" de "+dates.get_month(initial_date.month)+" </b>"
	ans += "entre las "
	ans += "<b>"+str(initial_date.hour)+":"+add0(str(initial_date.minute))+"</b> y "
	ans += "<b>"+str(final_date.hour)+":"+add0(str(final_date.minute))+" horas.</b>"
	ans += "<br><br>"
	ans += "Este evento se llevará a cabo en "
	ans += "<b>"+place+".</b>"
	ans += "<br><br>"
	# ans += "<form action ='calendart.herokuapp.com/delete_event' method='get'>"
	# ans += "<input type='hidden' name='id_calendar' value='"+mail_creator+"'>"
	# ans += "<input type='hidden' name='id_event' value='"+event_place['id']+"'>"
	# ans += "Si no ocupara la sala por favor presione el siguiente boton para que otros la puedan ocupar:"
	# ans += '<input value="Liberar la sala" type="submit"/>'
	# ans += "</form><br>"
	#formulario para pedir que se borre evento
	ans += "Si el evento no va a ocurrir, o no vas a utilizar la sala, por favor libérala para que otros la puedan ocupar."
	ans += "<br><br>"
	ans += "Edita el evento en el siguiente <b><a href="+link_owner+">enlace</a>. </b>"
	ans += "<br><br>"
	ans += "De confirmar la sala, omita este correo."
	ans += "<br><br><br>"
	ans += "PyT Techo "+random_face()
	return ans





