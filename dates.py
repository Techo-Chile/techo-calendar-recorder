from datetime import datetime, timedelta


def get_uct_date(server_date_init):
	divided = server_date_init.split('T')

	hours = divided[1].split('-')

	server_hour = hours[0]
	delta = int(hours[1].split(':')[0])

	server_date = divided[0]+' '+server_hour
	return datetime.strptime(server_date, '%Y-%m-%d %H:%M:%S') + timedelta(hours=delta) - timedelta(hours=3)

def get_month(number_mont):
	months = {1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo',
			6:'Junio', 7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre',
			11:'Noviembre', 12:'Diciembre'}
	return months[number_mont]

