#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from hr_2020_app.hr_2020_routes import (
    HealthApi,
    ServiceStatusApi,
    TouristSpotByIdResource,
    TouristSpotResource,
    UserByUsernameResource,
    UserListResource,
    UserResource)


app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app, resource={r"/*": {"origins": "*"}})

app.config['LOGGER_NAME'] = 'hackinrio_2020'

api = Api(app, prefix='/api')
api.add_resource(HealthApi, '/healthcheck', '/healthcheck/')
api.add_resource(ServiceStatusApi, '/status', '/status/')

api.add_resource(TouristSpotByIdResource,
                 '/tourist-spot/<string:spot_id>',
                 '/tourist-spot/<string:spot_id>/',
                 '/tourist-spot/id/<string:spot_id>')
api.add_resource(TouristSpotResource,
                 '/tourist-spot', '/tourist-spot/')

api.add_resource(UserByUsernameResource,
                 '/user/username/<string:username>',
                 '/user/username/<string:username>/')
api.add_resource(UserListResource, '/user', '/user/')
api.add_resource(UserResource,
                 '/user/<string:user_id>',
                 '/user/<string:user_id>/',
                 '/user/id/<string:user_id>',
                 '/user/id/<string:user_id>/')
