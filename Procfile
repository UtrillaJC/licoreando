% prepara el repositorio para su despliegue. 
release: sh -c 'python manage.py sqlflush | python manage.py dbshell && python manage.py makemigrations && python manage.py migrate  && python manage.py loaddata data.json'
web: sh -c 'gunicorn Licoreando.wsgi --log-file -'