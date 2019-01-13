DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

STATIC_ROOT = '/app/static/'
MEDIA_ROOT = '/app/static/media/'
ALLOWED_HOSTS = ['*']

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

BASEURL = 'http://localhost:9000'

APIS = {
    'authentication': 'http://localhost:9000',
    'base': 'http://localhost:9000',
    'booth': 'http://localhost:9000',
    'census': 'http://localhost:9000',
    'mixnet': 'http://localhost:9000',
    'postproc': 'http://localhost:9000',
    'store': 'http://localhost:9000',
    'visualizer': 'http://localhost:9000',
    'voting': 'http://localhost:9000',
}
