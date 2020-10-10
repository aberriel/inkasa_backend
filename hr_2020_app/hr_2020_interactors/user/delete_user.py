from hr_2020_app.hr_2020_adapters import UserAdapter
from hr_2020_app.hr_2020_domain import User
import logging


class DeleteUserException(BaseException):
    pass


class UserNotFoundException(BaseException):
    pass


class DeleteUserRequestModel:
    def __init__(self, json_data):
        self.username = json_data['username']


class DeleteUserResponseModel:
    def __init__(self, deleted_id):
        self.deleted_id = deleted_id

    def __call__(self):
        return self.deleted_id


class DeleteUserInteractor:
    def __init__(self, user_adapter: UserAdapter,
                 request: DeleteUserRequestModel):
        self.user_adapter = user_adapter
        self.request = request
        self.logger = logging.getLogger(__name__)

    def get_user(self):
        user_data = self.user_adapter.filter(username__eq=self.request.username)
        return user_data

    def run(self):
        try:
            user_data = self.get_user()
            if not user_data:
                raise UserNotFoundException(f'User {self.request.username} already deleted or never created')
            self.user_adapter.delete(user_data._id)
            response = DeleteUserResponseModel(user_data._id)
            return response
        except Exception as exc:
            msg = f'Error during delete user: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise DeleteUserException(msg)
