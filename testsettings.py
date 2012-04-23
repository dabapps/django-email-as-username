DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'emailusernames',
)

AUTHENTICATION_BACKENDS = (
    'emailusernames.backends.EmailAuthBackend',
)
