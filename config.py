from decouple import config


class Config:
	DEBUG = True
	ENVIRONMENT = config('FLASK_CONFIG', 'development')
	FLASK_APP = config('FLASK_APP', None)
	FLASK_DEBUG = config('FLASK_DEBUG', 1)

	MONGODB_URL = config('MONGODB_URL', 'mongodb+srv://{username}:{password}@coop0.xxx2q.mongodb.net/')
	MONGODB_DATABASE = config('MONGODB_DATABASE', 'hackinrio2020')
	MONGODB_USERNAME = config('MONGODB_USERNAME', 'root')
	MONGODB_PASSWORD = config('MONGODB_PASSWORD', 'hackinrio_2020')

	TOURIST_SPOT_TABLE_NAME = config('TOURIST_SPOT_TABLE_NAME', 'tourist_spot')
	USER_TABLE_NAME = config('USER_TABLE_NAME', 'user')

	TOKEN_SECRET_KEY = config('TOKEN_SECRET_KEY', 'secret_hack_2020')
	LOG_PATH = config('LOG_PATH', '/var/log/supervisor')
	LOGGER_STDOUT_LEVEL = config('LOGGER_STDOUT_LEVEL', 'DEBUG')
	LOGGER_STDERR_LEVEL = config('LOGGER_STDERR_LEVEL', 'DEBUG')


current_config = Config()
