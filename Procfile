% Prepare to release
release: sh -c 'cd decide && python manage.py migrate'
% Launch!
web: sh -c 'cd decide && gunicorn decide.wsgi --log-file -'
