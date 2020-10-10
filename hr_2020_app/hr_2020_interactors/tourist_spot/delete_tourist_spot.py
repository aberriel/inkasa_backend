from hr_2020_app.hr_2020_adapters import TouristSpotAdapter


class DeleteTouristSpotException(BaseException):
    pass


class TouristSpotNotExistsException(BaseException):
    pass


class DeleteTouristSpotRequestModel:
    def __init__(self, json_data):
        self.tourist_spot_id = json_data['tourist_spot_id']


class DeleteTouristSpotResponseModel:
    def __init__(self, deleted_id):
        self.deleted_id = deleted_id

    def __call__(self):
        return self.deleted_id


class DeleteTouristSpotInteractor:
    def __init__(self, adapter: TouristSpotAdapter,
                 request: DeleteTouristSpotRequestModel):
        self.adapter = adapter
        self.request = request

    def check_if_tourist_spot_exists(self):
        tourist_spot = self.adapter.get_by_id(self.request.tourist_spot_id)
        if not tourist_spot:
            raise TouristSpotNotExistsException(
                f'Spot {self.request.tourist_spot_id} does not exists.')

    def run(self):
        try:
            self.check_if_tourist_spot_exists()
            delete_result = self.adapter.delete(self.request.tourist_spot_id)
            response = DeleteTouristSpotResponseModel(delete_result)
            return response
        except Exception as exc:
            msg = f'Error during delete tourist spot: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise DeleteTouristSpotException(msg)
