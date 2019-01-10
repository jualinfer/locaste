% Prepare to release
release: sh -c 'cd decide && python manage.py migrate && python manage.py loaddata initial_data'
% Launch!
web: sh -c 'cd decide && gunicorn decide.wsgi --log-file -'
