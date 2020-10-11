from hr_2020_app.hr_2020_adapters import UserAdapter
from hr_2020_app.hr_2020_domain import User
from hr_2020_app.hr_2020_interactors.user import UserNotFoundException


class UpdateUserPasswordException(BaseException):
    pass


class UpdateUserPasswordRequestModel:
    def __init__(self, json_data):
        self.password = json_data['password']
        self.user_id = json_data['user_id']


class UpdateUserPasswordResponseModel:
    def __init__(self, user_id):
        self.user_id = user_id

    def __call__(self):
        return self.user_id


class UpdateUserPasswordInteractor:
    def __init__(self, adapter: UserAdapter,
                 request: UpdateUserPasswordRequestModel):
        self.adapter = adapter
        self.request = request

    def get_user(self):
        user_found = self.adapter.get_by_id(self.request.user_id)
        if not user_found:
            raise UserNotFoundException(f'User {self.request.user_id} not found')
        user_found.set_adapter(self.adapter)
        return user_found

    def update_user(self, user_data: User):
        user_data.set_password(self.request.password)
        return user_data.save()

    def run(self):
        try:
            user_data = self.get_user()
            self.update_user(user_data)
            response = UpdateUserPasswordResponseModel(self.request.user_id)
            return response
        except Exception as exc:
            msg = f'Error during update user password: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise UpdateUserPasswordException(msg)
