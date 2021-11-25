import environ
env = environ.Env()
environ.Env.read_env(env('DJANGO_ENV_DIR'))
from .settings import *


DEBUG = True 

DATABASES['default'].update({
    'HOST': env('MYSQL_HOST'),
    'NAME':  env('MYSQL_DATABASE'),
    'USER': env('MYSQL_USER'),
    'PASSWORD': env('MYSQL_PASSWORD'),
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
