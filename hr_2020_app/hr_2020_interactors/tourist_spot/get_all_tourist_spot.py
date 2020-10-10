from hr_2020_app.hr_2020_adapters import TouristSpotAdapter
from hr_2020_app.hr_2020_domain import TouristSpot
from typing import List

import logging


class GetAllTouristSpotException(BaseException):
    pass


class GetAllTouristSpotResponseModel:
    def __init__(self, tourist_spots: List[TouristSpot]):
        self.tourist_spots = tourist_spots

    def __call__(self):
        return [x.to_json() for x in self.tourist_spots]


class GetAllTouristSpotInteractor:
    def __init__(self, tourist_spot_adapter: TouristSpotAdapter):
        self.tourist_spot_adapter = tourist_spot_adapter
        self.logger = logging.getLogger(__name__)

    def run(self):
        try:
            tourist_spot_list = self.tourist_spot_adapter.list_all()
            return GetAllTouristSpotResponseModel(tourist_spot_list)
        except Exception as exc:
            msg = f'Error during get all users: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise GetAllTouristSpotException(msg)