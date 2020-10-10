from .operating_schedule import OperatingSchedule, WorkTime
from hr_2020_app.hr_2020_domain.basic_entity import BasicEntity
from hr_2020_app.hr_2020_domain.basic_value import BasicValue
from marshmallow import fields, post_load
from typing import List


class Address(BasicValue):
    def __init__(self,
                 street: str,
                 neighborhood: str,
                 city: str,
                 state: str,
                 street_number: str = 'S/N',
                 postal_code: str = None,
                 complement: str = None):
        self.street = street
        self.street_number = street_number
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.postal_code = postal_code

    def to_string(self):
        return f'{self.street}, {self.street_number}, ' \
               f'{self.complement} - {self.neighborhood}, {self.city} - ' \
               f'{self.state}, {self.postal_code}'

    class Schema(BasicValue.Schema):
        street = fields.String(required=True, allow_none=False)
        street_number = fields.String(required=True, allow_none=False, default='S/N')
        complement = fields.String(required=False, allow_none=True)
        neighborhood = fields.String(required=True, allow_none=False)
        city = fields.String(required=True, allow_none=False)
        state = fields.String(required=True, allow_none=False)
        postal_code = fields.String(required=False, allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return Address(**data)


class TouristSpot(BasicEntity):
    def __init__(self,
                 name: str,
                 telephone: str,
                 address: Address,
                 operating_schedules: list = None,
                 description: str = None,
                 web_page: str = None,
                 _id = None):
        super(TouristSpot, self).__init__(_id=_id)
        self.name = name
        self.description = description
        self.telephone = telephone
        self.address = address
        self.operating_schedules: List[OperatingSchedule] = \
            operating_schedules if operating_schedules else []
        self.web_page = web_page

    class Schema(BasicEntity.Schema):
        name = fields.String(required=True, allow_none=False)
        description = fields.String(required=False, allow_none=True)
        telephone = fields.String(required=True, allow_none=False)
        address = fields.Nested(Address.Schema, required=True, allow_none=False)
        operating_schedules = fields.Nested(
            OperatingSchedule.Schema,
            required=False,
            allow_none=True,
            many=True)
        web_page = fields.String(required=False, allow_none=True)

        @post_load
        def post_load(self, data, many, partial):
            return TouristSpot(**data)
