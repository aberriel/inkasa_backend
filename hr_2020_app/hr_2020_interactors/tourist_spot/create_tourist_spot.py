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
        self.name = json_data.get('name')
        self.description = json_data.get('description', None)
        self.address = json_data.get('address')
        self.telephone = json_data.get('telephone')
        self.web_page = json_data.get('web_page')
        self.operating_schedule = json_data.get('operating_schedule', None)


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

    def mount_tourist_spot(self):
        address = Address.from_json(self.request.address)
        operating_schedule = OperatingSchedule.from_json(self.request.operating_schedule)
        tourist_spot = TouristSpot(
            name=self.request.name,
            telephone=self.request.telephone,
            address=address,
            operating_schedule=operating_schedule,
            description=self.request.description,
            web_page=self.request.web_page)
        return tourist_spot

    def save_tourist_spot(self, tourist_spot: TouristSpot):
        tourist_spot.set_adapter(self.adapter)
        return tourist_spot.save()

    def run(self):
        try:
            tourist_spot = self.mount_tourist_spot()
            save_result = self.save_tourist_spot(tourist_spot)
            response = CreateTouristSpotResponseModel(save_result)
            return response
        except Exception as exc:
            msg = f'Error during create tourist spot: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise CreateTouristSpotException(msg)