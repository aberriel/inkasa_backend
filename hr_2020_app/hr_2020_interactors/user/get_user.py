from hr_2020_app.hr_2020_adapters import UserAdapter

import logging


class GetUserException(BaseException):
    pass


class GetUserRequestModel:
    def __init__(self, json_data):
        self.user_id = json_data['user_id']


class GetUserResponseModel:
    def __init__(self, user_data):
        self.user_data = user_data

    def __call__(self):
        if not self.user_data:
            return None
        return self.user_data.to_json()


class GetUserInteractor:
    def __init__(self,
                 user_adapter: UserAdapter,
                 request: GetUserRequestModel):
        self.user_adapter = user_adapter
        self.request = request
        self.logger = logging.getLogger(__name__)

    def run(self):
        try:
            user_found = self.user_adapter.get_by_id(self.request.user_id)
            return GetUserResponseModel(user_found)
        except Exception as exc:
            msg = f'Error during getting user: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise GetUserException(msg)
