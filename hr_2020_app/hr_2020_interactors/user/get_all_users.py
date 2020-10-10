from hr_2020_app.hr_2020_adapters import UserAdapter
from hr_2020_app.hr_2020_domain import User
from typing import List

import logging


class GetAllUsersException(BaseException):
    pass


class GetAllUsersResponseModel:
    def __init__(self, user_list):
        self.user_list: List[User] = user_list

    def __call__(self):
        result = list()
        for user in self.user_list:
            user_json = user.to_json()
            del user_json['password']
            result.append(user_json)
        return result


class GetAllUsersInteractor:
    def __init__(self, user_adapter: UserAdapter):
        self.user_adapter = user_adapter
        self.logger = logging.getLogger(__name__)

    def run(self):
        print('GetAllUsersInteractor.run -> Entrando')
        try:
            print('GetAllUsersInteractor.run -> Pegando todos os usuários')
            user_list = self.user_adapter.list_all()
            print('GetAllUsersInteractor.run -> Retornando no response')
            return GetAllUsersResponseModel(user_list)
        except Exception as exc:
            print('GetAllUsersInteractor.run -> Ocorreu um erro')
            msg = f'Error during get all users: ' \
                  f'{exc.__class__.__name__}: {exc}'
            print('GetAllUsersInteractor.run -> Mensagem de erro: ' + msg)
            self.logger.error(msg)
            raise GetAllUsersException(msg)
