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

BASEURL = 'http://localhost'

APIS = {
    'authentication': 'http://localhost',
    'base': 'http://localhost',
    'booth': 'http://localhost',
    'census': 'http://localhost',
    'mixnet': 'http://localhost',
    'postproc': 'http://localhost',
    'store': 'http://localhost',
    'visualizer': 'http://localhost',
    'voting': 'http://localhost',
}
