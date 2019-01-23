ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'licoreando',
        'USER': 'licoreando',
        'PASSWORD': 'licoreando',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256