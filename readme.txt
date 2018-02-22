para enviar mails:

$ sudo pip install -r requirements.txt

$ python app.py

para activar el appweb que recibe los request:

$ python Web_Request.py

IMPORTANTE:
si se hace correr en un servidor, hay que agregar la flag --noauth_local_webserver:
ej:

$ python Web_Request.py --noauth_local_webserver


informacion de los archivos:

Find_Events:
	Se encarga de conectarse con la api de google calendar.
	metodos:
		set_credentials: crea las credenciales para acceder a la api.
			en caso ed que ya esten almacenadas, las utiliza
		get_events: retorna una lista de eventos de un determinado calendario
			en un rango determinado de fechas
		get_event: retorna un determinado evento de un calendario, para esto
			requiere el id del candario y el id del evento
		delete_event: elimina un determinado evento de un determinado calendario
			requiere lo mismo que get_event
Sender_Mail:
	Se encarga de conectarse con la api de gmail y enviar mails
	metodos:
		set_credentials: crea las credenciales para acceder a la api.
			en caso ed que ya esten almacenadas, las utiliza
		create_message: recibe un mail que corresponde a la persona que envia, 
			otro mail que corresponde a la persona que lo envia, un mensaje,
			codifica y comprime esto para luego enviarlo
		send_message: recibe un correo y un mensaje codificado.
			Envia el mensaje desde ese correo.

Messages:
	se encarga de crear un texto con el mail (y con html)

dates:
	hace el trabajo de fechas para que se coordinen las fechas de chile 
	con las fechas del servidor.

app:
	al hacerla correr envia los mails a todas las personas que tienen algun evento
	agendado y que a la vez hayan adquirido la propiedad de la salas.


Web_Request: 
	app web que recibe los request del formulario creado en Messages, si cambia
	el servidor donde esta alojado ir a la linea 65 de Messages y cambiar 
	action del formulario



Scheduler:
	El programa utiliza crontab para hacer un daemon que lanza el programa a la hora
	indicada del día indicado.

	Para editar el archivo de crontab que contiene el schedule, en la terminal ejecute el
	comando:

		crontab -e

	edite el archivo, donde los primeros 5 argumentos indican el horario:
	minuto, hora, "día del mes", mes, "dia de la semana", separados por un espacio

	por ejemplo, para ejecutarlo lunes a viernes, a las 5 de la tarde

		0 17 * * 1-5 python /root/git/techo-calendar-recorder/app.py

	OJO: se ocupa la hora de digital ocean, que está 3 horas adelantada, por lo tanto, el
	comando sería:

		0 20 * * 1-5 python /root/git/techo-calendar-recorder/app.py

	Más información:
		https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-on-a-vps