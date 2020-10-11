from config import Config
from flask import request
from flask_restful import Resource
from hr_2020_app.hr_2020_adapters import UserAdapter
from hr_2020_app.hr_2020_interactors import (
    CheckUserCredentialsException,
    CheckUserCredentialsInteractor,
    CheckUserCredentialsRequestModel,
    CheckUserCredentialsResponseModel)


class AuthenticationApi(Resource):
    def _get_user_adapter(self):
        config = Config()
        adapter = UserAdapter(
            table_name=config.USER_TABLE_NAME,
            db_name=config.MONGODB_DATABASE,
            db_url=config.MONGODB_URL,
            db_username=config.MONGODB_USERNAME,
            db_password=config.MONGODB_PASSWORD)
        return adapter

    def post(self):
        get_params = request.get_json()
        try:
            request_data = CheckUserCredentialsRequestModel(get_params)
            interactor = CheckUserCredentialsInteractor(
                adapter=self._get_user_adapter(),
                request=request_data)
            response = interactor.run()()
            if not response:
                return {
                    'status': 'error',
                    'message': 'access denied'
                }, 401
            return { 'status': 'ok' }, 200
        except Exception as e:
            return {
                'status': 'error',
                'error_msg': str(e)
            }, 500
