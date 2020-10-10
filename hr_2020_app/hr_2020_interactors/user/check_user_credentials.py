from hr_2020_app.hr_2020_adapters import UserAdapter
from hr_2020_app.hr_2020_domain import User

import logging


class CheckUserCredentialsException(BaseException):
    pass


class IncorrectCredentialsException(BaseException):
    pass


class CheckUserCredentialsRequestModel:
    def __init__(self, json_data):
        self.username = json_data['username']
        self.password = json_data['password']


class CheckUserCredentialsResponseModel:
    def __init__(self, can_authenticate: bool):
        self.can_authenticate = can_authenticate

    def __call__(self):
        return self.can_authenticate


class CheckUserCredentialsInteractor:
    def __init__(self, adapter: UserAdapter,
                 request: CheckUserCredentialsRequestModel):
        self.adapter = adapter
        self.request = request
        self.logger = logging.getLogger(__name__)

    def get_user(self):
        user_data = self.adapter.filter(username__eq=self.request.username)
        if not user_data:
            raise IncorrectCredentialsException(f'User {self.request.username} not found')
        return user_data

    def run(self):
        try:
            user_data: User = self.get_user()
            check_result = user_data.authenticate(
                login=self.request.username,
                password=self.request.password)
            response = CheckUserCredentialsResponseModel(check_result)
            return response
        except Exception as exc:
            msg = f'Error during check credentials: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise CheckUserCredentialsException(msg)
