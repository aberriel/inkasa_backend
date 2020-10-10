from hr_2020_app.hr_2020_adapters import TouristSpotAdapter
from hr_2020_app.hr_2020_domain import TouristSpot

import logging


class GetTouristSpotException(BaseException):
    pass


class GetTouristSpotRequestModel:
    def __init__(self, json_data):
        self.spot_id = json_data['spot_id']


class GetTouristSpotResponseModel:
    def __init__(self, tourist_spot: TouristSpot):
        self.tourist_spot = tourist_spot

    def __call__(self):
        if self.tourist_spot:
            return self.tourist_spot.to_json()
        return None


class GetTouristSpotInteractor:
    def __init__(self, tourist_spot_adapter: TouristSpotAdapter,
                 request: GetTouristSpotRequestModel):
        self.tourist_spot_adapter = tourist_spot_adapter
        self.request = request
        self.logger = logging.getLogger(__name__)

    def run(self):
        try:
            spot_found = self.tourist_spot_adapter.get_by_id(self.request.spot_id)
            return GetTouristSpotResponseModel(spot_found)
        except Exception as exc:
            msg = f'Error during getting user: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise GetTouristSpotException(msg)
