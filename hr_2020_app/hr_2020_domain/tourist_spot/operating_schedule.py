from datetime import time
from enum import Enum
from hr_2020_app.hr_2020_domain.basic_value import BasicValue
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from typing import List


class WeekDay(Enum):
    SUNDAY = 'SUNDAY'
    MONDAY = 'MONDAY'
    THUESDAY = 'THUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY'
    SATURDAY = 'SATURDAY'


class WorkTime(BasicValue):
    def __init__(self,
                 opening_time: time,
                 closing_time: time):
        self.opening_time = opening_time
        self.closing_time = closing_time

    class Schema(BasicValue.Schema):
        opening_time = fields.Time(required=True, allow_none=False)
        closing_time = fields.Time(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return WorkTime(**data)


class OperatingSchedule(BasicValue):
    def __init__(self,
                 week_day: WeekDay,
                 work_times: list = None):
        self.week_day = week_day
        self.work_times: List[WorkTime] = work_times if work_times else []

    class Schema(BasicValue.Schema):
        week_day = EnumField(
            WeekDay,
            required=True,
            allow_none=False)
        work_times = fields.Nested(WorkTime.Schema, many=True)

        @post_load
        def post_load(self, data, many, partial):
            return OperatingSchedule(**data)