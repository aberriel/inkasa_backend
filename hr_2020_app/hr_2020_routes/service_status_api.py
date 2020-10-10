from config import Config
from flask_restful import Resource


class ServiceStatusApi(Resource):
    def get(self):
        config = Config()
        return {
            'environment_variables': {
                'MONGODB_URL': config.MONGODB_URL,
                'MONGODB_DATABASE': config.MONGODB_DATABASE,
                'MONGODB_USERNAME': config.MONGODB_USERNAME,
                'MONGODB_PASSWORD': config.MONGODB_PASSWORD,
                'USER_TABLE_NAME': config.USER_TABLE_NAME,
                'FLASK_APP': config.FLASK_APP,
                'FLASK_DEBUG': config.FLASK_DEBUG,
                'ENVIRONMENT': config.ENVIRONMENT,
                'LOG_PATH': config.LOG_PATH
            }
        }
