# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = 'v+(z=4nvd&zs5ldc27^4yk1f%wtr@n2f(+2qy*n*cto@2#*pv!'
NEVERCACHE_KEY = "(!org&1*e%x!6y61ijp%@41(#_b6@$2db4*pw4x%))3hohmw*o"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mysite',
        'USER': 'vwaj',
        'PASSWORD': 'Startupisu',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# any settings specific to local environment can be overridden in `local_settings.py`
try:
    from mysite.local_settings import *
except ImportError:
    pass
