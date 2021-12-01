import environ
env = environ.Env()
environ.Env.read_env(env('DJANGO_ENV_DIR'))
from .settings import *


DEBUG = True 

DATABASES['default'].update({
    'ENGINE': 'django.db.backends.mysql',
    'HOST': env('MYSQL_HOST'),
    'NAME':  env('NM_DATABASE'),
    'USER': env('NM_USER'),
    'PASSWORD': env('NM_PASSWORD'),
})

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(message)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins', 'console', ],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console', ],
            'propagate': True,
            'level': 'INFO',
        }
    }
}
ALLOWED_HOSTS = ['.newsmaker.tv']
STATIC_ROOT = '/var/www/nm/moo_o/static'

