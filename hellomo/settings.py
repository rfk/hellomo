
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'je%ebi$409g^3czu@kqkx@qcis1!7ld*f14-&*&vf@v*8*&2t2'
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.file'

ROOT_URLCONF = 'hellomo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'hellomo/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hellomo.wsgi.application'

STATIC_URL = '/static/'

OIDC_CLIENT_CONFIG = {
  'https://oidc.dev.lcip.org': {
    'client_id': 'insertme',
    'client_secret': 'secrethere',
  }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
