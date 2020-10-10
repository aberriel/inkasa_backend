from hr_2020_app.hr_2020_adapters import UserAdapter
from hr_2020_app.hr_2020_domain import User

import logging


class CreateUserException(BaseException):
    pass


class UsernameAlreadyExistsException(BaseException):
    pass


class CreateUserRequestModel:
    def __init__(self, json_data):
        self.username = json_data['username']
        self.password = json_data['password']


class CreateUserResponseModel:
    def __init__(self, user_id):
        self.user_id = user_id

    def __call__(self):
        return self.user_id


class CreateUserInteractor:
    def __init__(self, user_adapter: UserAdapter,
                 request: CreateUserRequestModel):
        self.user_adapter = user_adapter
        self.request = request
        self.logger = logging.getLogger(__name__)

    def check_username(self):
        user_old = self.user_adapter.filter(username__eq=self.request.username)
        if user_old:
            raise UsernameAlreadyExistsException(f'Username {self.request.username} is in use.')

    def mount_user(self):
        user_data = User(
            username=self.request.username,
            password=self.request.password)
        user_data.set_adapter(self.user_adapter)
        return user_data

    def save_user(self, user_data: User):
        user_data.set_password(self.request.password)
        return user_data.save()

    def run(self):
        try:
            self.check_username()
            user_data = self.mount_user()
            save_result = self.save_user(user_data)
            response = CreateUserResponseModel(
                user_id=save_result)
            return response
        except Exception as exc:
            msg = f'Error during create user: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise CreateUserException(msg)