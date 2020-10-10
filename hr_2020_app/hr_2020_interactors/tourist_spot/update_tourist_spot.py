from hr_2020_app.hr_2020_adapters import TouristSpotAdapter
from hr_2020_app.hr_2020_domain import (
    Address,
    OperatingSchedule,
    TouristSpot)

import logging


class UpdateTouristSpotException(BaseException):
    pass


class UpdateTouristSpotRequestModel:
    def __init__(self, json_data):
        self.json_data = json_data


class UpdateTouristSpotResponseModel:
    def __init__(self, tourist_spot_id):
        self.tourist_spot_id = tourist_spot_id

    def __call__(self):
        return self.tourist_spot_id


class UpdateTouristSpotInteractor:
    def __init__(self, adapter: TouristSpotAdapter,
                 request: UpdateTouristSpotRequestModel):
        self.adapter = adapter
        self.request = request
        self.logger = logging.getLogger(__name__)

    def save_tourist_spot(self, tourist_spot: TouristSpot):
        tourist_spot.set_adapter(self.adapter)
        return tourist_spot.save()

    def run(self):
        try:
            tourist_spot = TouristSpot.from_json(self.request.json_data)
            save_result = self.save_tourist_spot(tourist_spot)
            response = UpdateTouristSpotResponseModel(save_result)
            return response
        except Exception as exc:
            msg = f'Error during update tourist spot: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise UpdateTouristSpotException(msg)
