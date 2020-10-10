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
        self.name = json_data['name']
        self.description = json_data['description']
        self.telephone = json_data['telephone']
        self.address = json_data['address']
        self.web_page = json_data['web_page']
        self.operating_schedule = json_data['operating_schedule']


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
        tourist_spot.set_adapter(self.adapter)
        return tourist_spot

    def run(self):
        try:
            tourist_spot = self.mount_tourist_spot()
            update_result = tourist_spot.save()
            response = UpdateTouristSpotResponseModel(update_result)
            return response
        except Exception as exc:
            msg = f'Error during update tourist spot: ' \
                  f'{exc.__class__.__name__}: {exc}'
            self.logger.error(msg)
            raise UpdateTouristSpotException(msg)
