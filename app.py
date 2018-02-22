from Sender_Mail import *
from Find_Events import *
import Messages
import datetime

def main():

	finder = Find_Events()
	finder.set_credentials()
	#inicializa objeto que se encarga de administrar los eventos
	
	sender = Sender_Mail()
	sender.set_credentials()
	#inicializa objeto que se encarga de administrar los mails

	calendars = {'Biblioteca':'techo.org_333634383939383839@resource.calendar.google.com',
				'Padre Hurtado': 'techo.org_3930373433393731353036@resource.calendar.google.com',
				'Teresa de Calcuta': 'techo.org_2d3932343130383736363634@resource.calendar.google.com',
				'Salon Latinoamericano': 'techo.org_34363138343732312d373236@resource.calendar.google.com'}
	#lista de calendarios involucrados, para agregar mas calendarios solo hay que ponerle el nombre
	#que desee agregar y agregar el id del calendario.

	now = datetime.datetime.utcnow() 

	now_00 = now - datetime.timedelta(hours = now.hour - 3, minutes=now.minute)
	tomorrow_00 = now_00 + datetime.timedelta(days = 1) 
	tomorrow_2359 = tomorrow_00 + datetime.timedelta(hours=23, minutes = 59)

	tomorrow_00 = tomorrow_00.isoformat() + 'Z'
	tomorrow_2359 = tomorrow_2359.isoformat() + 'Z'

	#trabajo de fechas, el servidor funciona con la hora UCT, a esta hora se le deben
	#quitar 3 horas para que calcen todos los eventos en un dia.
	#IMPORTANTE: la fecha corresponde para los eventos del dia de mañana
	
	total_events = 0
	private_events = 0
	events_without_place = 0
	events_with_mail = 0
	#contadores de eventos 

	for value in calendars:
		#itera entre los calendarios de calendars
		print("Enviando correos de "+value)


		events = finder.get_events(calendars[value],tomorrow_00,tomorrow_2359)
		#busca todos los eventos del dia de mañana


		
		for event in events:
			#se recorre la lista de eventos de la sala (recurso)
			total_events += 1
			place_is_free = True

			is_private = False
			if 'visibility'in event:
				if event['visibility'] == 'private':
					private_events += 1
					is_private = True
			#comprueba que el evento no sea privado. En caso de ser privado se omite ya que 
			#no se puede tener informacion de un evento privado

			if not is_private:

				for val in event['attendees']:
					if 'resource' in val:
						if val['responseStatus'] == 'declined':
							events_without_place +=1
							place_is_free = False
					#se comprueba que el evento SI este utilizando la sala (el recurso)
					#en caso de que no este utilizando la sala, se omite ya que no requiere
					#confirmacion.

				event_creator = event['creator']['email']
				event_id = event['id']
				#email del creador e id del evento.

				if(place_is_free):
					events_with_mail += 1
					
					print('Enviando correo a '+event_creator+" por id evento :")
					print(event['id'])

					event_owner = finder.get_event(event_creator,event_id)
					#se busca el evento del dueño, este evento es diferente al del recurso
					#pero contiene la misma id
					
					message_text = Messages.create_message(event, event_owner, calendars[value])
					#se crea el mensaje del email

					#message_b64 = sender.create_message('PyT Chile <pyt.chile@techo.org>',event_creator,'Confirmar Sala Techo', message_text)
					message_b64 = sender.create_message('PyT Chile <pyt.chile@techo.org>','pyt.chile@techo.org','Confirmar Sala Techo', message_text)
					#se crea el email, emisor, receptor, asunto y el mensaje

					sender.send_message('pyt.chile@techo.org',message_b64)
					#se envia el mail

		print('-----------------------------------')
	print('Eventos Privados: '+str(total_events))
	print('Eventos sin lugar: '+str(total_events))
	print('Mails Enviados (eventos espera confirmacion): '+str(events_with_mail))
	print('Total Eventos: '+str(total_events))

	#se imprime la informacion de los eventos

if __name__ == '__main__':
    main()