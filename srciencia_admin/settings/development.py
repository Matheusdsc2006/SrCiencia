from .settings import*

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY= config('SECRET_KEY')
ALLOWED_HOSTS = ['127.0.0.1']

DATABASES={
'default':{
'ENGINE':'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
}