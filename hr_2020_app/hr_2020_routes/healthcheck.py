from flask_restful import Resource
from hr_2020_app.utils.datetime_utils import aware_now


class HealthApi(Resource):
	def get(self):
		return {
			'status': 'ok',
			'time_check': aware_now().isoformat()
		}, 200
