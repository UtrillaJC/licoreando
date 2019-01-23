% prepara el repositorio para su despliegue. 
release: sh -c ' cd Licoreando && python manage.py sqlflush | python manage.py dbshell && python manage.py makemigrations && python manage.py migrate  && python manage.py loaddata data.json'
web: sh -c 'cd Licoreando && gunicorn Licoreando.wsgi --log-file -'