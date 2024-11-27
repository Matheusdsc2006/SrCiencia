from decouple import config

print(config('TEST_ENV', default='Funciona!'))
