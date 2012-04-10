DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'emailusernames',
    'django.contrib.auth',
    'django.contrib.contenttypes',
)

AUTHENTICATION_BACKENDS = (
    'emailusernames.backends.EmailAuthBackend',
)
