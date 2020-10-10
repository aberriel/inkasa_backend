from hr_2020_app.hr_2020_adapters import TouristSpotAdapter
from hr_2020_app.hr_2020_domain import (
    Address,
    OperatingSchedule,
    TouristSpot)

import logging


class CreateTouristSpotException(BaseException):
    pass


class CreateTouristSpotRequestModel:
    def __init__(self, json_data):
        self.json_data = json_data
        self.json_data['_id'] = ''


class CreateTouristSpotResponseModel:
    def __init__(self, spot_id):
        self.spot_id = spot_id

    def __call__(self):
        return self.spot_id


class CreateTouristSpotInteractor:
    def __init__(self, adapter: TouristSpotAdapter,
                 request: CreateTouristSpotRequestModel):
        self.adapter = adapter
        self.request = request
        self.logger = logging.getLogger(__name__)

    def save_tourist_spot(self, tourist_spot: TouristSpot):
        tourist_spot.set_adapter(self.adapter)
        return tourist_spot.save()

    def run(self):
        print('CreateTouristSpotInteractor.run -> Entrando')
        try:
            print('CreateTouristSpotInteractor.run -> Montando o TouristSpot')
            tourist_spot = TouristSpot.from_json(self.request.json_data)
            print('CreateTouristSpotInteractor.run -> Salvando no banco')
            save_result = self.save_tourist_spot(tourist_spot)
            print('CreateTouristSpotInteractor.run -> Montando o response')
            response = CreateTouristSpotResponseModel(save_result)
            print('CreateTouristSpotInteractor.run -> Retornano o response')
            return response
        except Exception as exc:
            msg = f'Error during create tourist spot: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise CreateTouristSpotException(msg)