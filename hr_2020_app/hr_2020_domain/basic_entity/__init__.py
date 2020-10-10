from marshmallow import Schema, fields
from uuid import uuid4

from hr_2020_app.hr_2020_domain.basic_value import BasicValue


class BasicEntity(BasicValue):
    def __init__(self, _id=None):
        self._id = _id or str(uuid4())
        self.adapter = None

    def set_adapter(self, adapter):
        self.adapter = adapter

    def save(self):
        my_id = self.adapter.save(self.to_json())
        return my_id

    def update(self):
        my_id = self.adapter.save(self.to_json())
        return my_id

    def delete(self):
        self.adapter.delete(self._id)

    def __eq__(self, other):
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)

    class Schema(Schema):
        _id = fields.String(required=True, allow_none=True)
