from Sender_Mail import *
from Find_Events import *
import Messages
import datetime

def main():

	finder = Find_Events()
	finder.set_credentials()
	
	sender = Sender_Mail()
	sender.set_credentials()

	calendars = {'Biblioteca':'techo.org_333634383939383839@resource.calendar.google.com',
				'Padre Hurtado': 'techo.org_3930373433393731353036@resource.calendar.google.com',
				'Teresa de Calcuta': 'techo.org_2d3932343130383736363634@resource.calendar.google.com',
				'Salon Latinoamericano': 'techo.org_34363138343732312d373236@resource.calendar.google.com'}
	
	now = datetime.datetime.utcnow() 

	now_00 = now - datetime.timedelta(hours = now.hour - 3, minutes=now.minute)
	tomorrow_00 = now_00 + datetime.timedelta(days = 1) 
	tomorrow_2359 = tomorrow_00 + datetime.timedelta(hours=23, minutes = 59)

	tomorrow_00 = tomorrow_00.isoformat() + 'Z'
	tomorrow_2359 = tomorrow_2359.isoformat() + 'Z'
	
	total_events = 0
	private_events = 0
	events_without_place = 0
	events_with_mail = 0

	for value in calendars:
		print("Enviando correos de "+value)


		events = finder.get_events(calendars[value],tomorrow_00,tomorrow_2359)

		
		for event in events:
			total_events += 1
			place_is_free = True

			is_private = False
			if 'visibility'in event:
				if event['visibility'] == 'private':
					private_events += 1
					is_private = True

			if not is_private:

				for val in event['attendees']:
					if 'resource' in val:
						if val['responseStatus'] == 'declined':
							events_without_place +=1
							place_is_free = False

				event_creator = event['creator']['email']
				event_id = event['id']

				if(place_is_free):
					events_with_mail += 1
					
					print('Enviando correo a '+event_creator+" por id evento :")
					print(event['id'])

					event_owner = finder.get_event(event_creator,event_id)
					
					'''if (event_creator == 'felipe.alamos@techo.org'):
						finder.service.events().delete(calendarId='felipe.alamos@techo.org', eventId = event['id']).execute()'''

					message_text = Messages.create_message(event, event_owner)

					message_b64 = sender.create_message('PyT Chile <pyt.chile@techo.org>','felipe.alamos@techo.org','Confirmar Sala Techo', message_text)

					sender.send_message('pyt.chile@techo.org',message_b64)
					return 0

		print('-----------------------------------')
	print('Eventos Privados: '+str(total_events))
	print('Eventos sin lugar: '+str(total_events))
	print('Mails Enviados (eventos espera confirmacion): '+str(events_with_mail))
	print('Total Eventos: '+str(total_events))

if __name__ == '__main__':
    main()