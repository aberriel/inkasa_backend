from hr_2020_app.hr_2020_adapters import UserAdapter
import logging


class GetUserByUsernameException(BaseException):
    pass


class GetUserByUsernameRequestModel:
    def __init__(self, json_data):
        self.username = json_data['username']


class GetUserByUsernameResponseModel:
    def __init__(self, user_data):
        self.user_data = user_data

    def __call__(self):
        if not self.user_data:
            return None
        return self.user_data.to_json()


class GetUserByUsernameInteractor:
    def __init__(self,
                 user_adapter: UserAdapter,
                 request: GetUserByUsernameRequestModel):
        self.user_adapter = user_adapter
        self.request = request
        self.logger = logging.getLogger(__name__)

    def run(self):
        try:
            print('GetUserByUsernameInteractor.run -> Entrando')
            print('GetUserByUsernameInteractor.run -> Obtendo a lista filtrada do banco')
            print('GetUserByUsernameInteractor.run -> username: ' + self.request.username)
            user_list = self.user_adapter.filter(username__eq=self.request.username)
            print('GetUserByUsernameInteractor.run -> len(user_list): ' + str(len(user_list)))
            print('GetUserByUsernameInteractor.run -> Recuperando o usuário')
            user_found = user_list[0] if user_list and len(user_list) > 0 else None
            print('GetUserByUsernameInteractor.run -> user_found: ' + str(user_found))
            print('GetUserByUsernameInteractor.run -> Montando o response e retornando')
            return GetUserByUsernameResponseModel(user_found)
        except Exception as exc:
            print('GetUserByUsernameInteractor.run -> Um erro ocorreu')
            msg = f'Error during get user: ' \
                  f'{exc.__class__.__name__}: {exc}'
            print('GetUserByUsernameInteractor.run -> Mensagem de erro: ' + msg)
            self.logger.error(msg)
            print('GetUserByUsernameInteractor.run -> Saindo com erro')
            raise GetUserByUsernameException(msg)
