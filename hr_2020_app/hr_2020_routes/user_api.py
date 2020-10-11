from config import Config
from flask import jsonify, request
from flask_restful import reqparse, Resource
from hr_2020_app.hr_2020_adapters import UserAdapter
from hr_2020_app.hr_2020_interactors import (
    CreateUserInteractor,
    CreateUserRequestModel,
    CreateUserResponseModel,
    DeleteUserInteractor,
    DeleteUserRequestModel,
    DeleteUserResponseModel,
    GetAllUsersInteractor,
    GetAllUsersResponseModel,
    GetUserInteractor,
    GetUserRequestModel,
    GetUserResponseModel,
    GetUserByUsernameInteractor,
    GetUserByUsernameRequestModel,
    GetUserByUsernameResponseModel,
    UpdateUserPasswordInteractor,
    UpdateUserPasswordRequestModel)

import traceback


class UserResourceBase(Resource):
    def _get_user_adapter(self):
        config_obj = Config()
        adapter = UserAdapter(
            table_name=config_obj.USER_TABLE_NAME,
            db_name=config_obj.MONGODB_DATABASE,
            db_url=config_obj.MONGODB_URL,
            db_username=config_obj.MONGODB_USERNAME,
            db_password=config_obj.MONGODB_PASSWORD)
        return adapter


class UserListResource(UserResourceBase):
    def get(self):
        try:
            interactor = GetAllUsersInteractor(user_adapter=self._get_user_adapter())
            response = interactor.run()
            return response(), 200
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
            request_obj = CreateUserRequestModel(post_params)
            interactor = CreateUserInteractor(
                request=request_obj,
                user_adapter=self._get_user_adapter())
            response = interactor.run()
            return response(), 201
        except Exception as exc:
            stack_trace = traceback.format_exc()
            return {
                'http_status': 500,
                'error': {
                    'stack_trace': stack_trace,
                    'message': str(exc)
                }}, 500


class UserResource(UserResourceBase):
    def get(self, user_id: str):
        try:
            request_json = {'user_id': user_id }
            request = GetUserRequestModel(json_data=request_json)
            interactor = GetUserInteractor(
                user_adapter=self._get_user_adapter(),
                request=request)
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

    def put(self, user_id: str):
        try:
            put_params = request.get_json()
            put_params['user_id'] = user_id
            request_obj = UpdateUserPasswordRequestModel(put_params)
            interactor = UpdateUserPasswordInteractor(
                adapter=self._get_user_adapter(),
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


class UserByUsernameResource(UserResourceBase):
    def get(self, username: str):
        try:
            request_json = {'username': username}
            request = GetUserByUsernameRequestModel(request_json)
            interactor = GetUserByUsernameInteractor(
                user_adapter=self._get_user_adapter(),
                request=request)
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

    def delete(self, username: str):
        try:
            delete_params = {'username': username}
            request_obj = DeleteUserRequestModel(
                json_data=delete_params)
            interactor = DeleteUserInteractor(
                user_adapter=self._get_user_adapter(),
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
