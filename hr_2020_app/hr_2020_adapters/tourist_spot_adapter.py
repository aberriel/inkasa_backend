from .basic_mongodb_adapter import BasicMongodbAdapter
from hr_2020_app.hr_2020_domain.tourist_spot import TouristSpot


class TouristSpotAdapter(BasicMongodbAdapter):
    def __init__(self, table_name: str,
                 db_name: str,
                 db_url: str,
                 db_username: str,
                 db_password: str):
        super(TouristSpotAdapter, self).__init__(
            table_name=table_name,
            db_name=db_name,
            db_url=db_url,
            db_username=db_username,
            db_password=db_password,
            adapted_class=TouristSpot)