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
            user_list = self.user_adapter.filter(username__eq=self.request.username)
            user_found = user_list[0] if user_list and len(user_list) > 0 else None
            return GetUserByUsernameResponseModel(user_found)
        except Exception as exc:
            msg = f'Error during get user: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise GetUserByUsernameException(msg)
