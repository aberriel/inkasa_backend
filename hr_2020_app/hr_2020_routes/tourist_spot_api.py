from config import Config
from flask import request
from flask_restful import Resource
from hr_2020_app.hr_2020_adapters import TouristSpotAdapter
from hr_2020_app.hr_2020_interactors import (
    CreateTouristSpotInteractor,
    CreateTouristSpotRequestModel,
    DeleteTouristSpotInteractor,
    DeleteTouristSpotRequestModel,
    GetAllTouristSpotInteractor,
    GetTouristSpotInteractor,
    GetTouristSpotRequestModel,
    UpdateTouristSpotInteractor,
    UpdateTouristSpotRequestModel)

import traceback


class TouristSpotResourceBase(Resource):
    def get_tourist_spot_adapter(self):
        config_obj = Config()
        return TouristSpotAdapter(
            table_name=config_obj.TOURIST_SPOT_TABLE_NAME,
            db_name=config_obj.MONGODB_DATABASE,
            db_url=config_obj.MONGODB_URL,
            db_username=config_obj.MONGODB_USERNAME,
            db_password=config_obj.MONGODB_PASSWORD)


class TouristSpotByIdResource(TouristSpotResourceBase):
    def get(self, spot_id):
        try:
            request_json = {'spot_id': spot_id}
            request_obj = GetTouristSpotRequestModel(request_json)
            interactor = GetTouristSpotInteractor(
                tourist_spot_adapter=self.get_tourist_spot_adapter(),
                request=request_obj)
            response = interactor.run()()
            if not response:
                return {
                    'http_status': 404,
                    'error': { 'message': 'NOT FOUND' }
                }, 404
            return response, 200
        except Exception as exc:
            stack_trace = traceback.format_exc()
            return {
                'http_status': 500,
                'error': {
                    'stack_trace': stack_trace,
                    'message': str(exc)
                }}, 500

    def delete(self, spot_id):
        try:
            request_json = {'tourist_spot_id': spot_id}
            request_obj = DeleteTouristSpotRequestModel(request_json)
            interactor = DeleteTouristSpotInteractor(
                adapter=self.get_tourist_spot_adapter(),
                request=request_obj)
            response = interactor.run()()
            return response, 201
        except Exception as exc:
            stack_trace = traceback.format_exc()
            return {
                'http_status': 500,
                'error': {
                    'stack_trace': stack_trace,
                    'message': str(exc)
                }}, 500


class TouristSpotResource(TouristSpotResourceBase):
    def get(self):
        try:
            interactor = GetAllTouristSpotInteractor(self.get_tourist_spot_adapter())
            response = interactor.run()()
            return response, 200
        except Exception as exc:
            stack_trace = traceback.format_exc()
            return {
                'http_status': 500,
                'error': {
                    'stack_trace': stack_trace,
                    'message': str(exc)
                }}, 500

    def post(self):
        try:
            post_params = request.get_json()
            request_obj = CreateTouristSpotRequestModel(post_params)
            interactor = CreateTouristSpotInteractor(
                adapter=self.get_tourist_spot_adapter(),
                request=request_obj)
            response = interactor.run()()
            return response, 200
        except Exception as exc:
            stack_trace = traceback.format_exc()
            return {
                'http_status': 500,
                'error': {
                    'stack_trace': stack_trace,
                    'message': str(exc)
                }}, 500

    def put(self):
        try:
            put_params = request.get_json()
            request_obj = UpdateTouristSpotRequestModel(put_params)
            interactor = UpdateTouristSpotInteractor(
                adapter=self.get_tourist_spot_adapter(),
                request=request_obj)
            response = interactor.run()(),
            return response, 201
        except Exception as exc:
            stack_trace = traceback.format_exc()
            return {
                'http_status': 500,
                'error': {
                    'stack_trace': stack_trace,
                    'message': str(exc)
                }}, 500
