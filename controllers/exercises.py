import logging
from odoo import http
from odoo.http import request, Response
from .auth import JWTAuth
from ._helpers import _http_success_response, _http_error_response
from odoo.exceptions import AccessDenied
_logger = logging.getLogger(__name__)

class ExercisesController(http.Controller):

    @http.route('/api/easy_apps/gym/exercises', type='http', auth="none", methods=['GET'], csrf=False)
    def get_exercises(self, **kwargs):
        """Retrieve a list of exercises"""
        try:
            #  Authenticate user using JWT
            user = JWTAuth.authenticate_request()

            #  Check if authentication failed
            if 'error' in user:
                return _http_error_response(user['error'], 401)  # Unauthorized

            #  Fetch all exercises
            exercises = request.env['easy_gym.exercises'].sudo().search([])

            #  Format response data
            exercise_list = [{
                'id': e.id,
                'name': e.name,
                'focus_area_id': e.focus_area_id.id if e.focus_area_id else None,
                'image': f"data:image/png;base64,{e.image.decode('utf-8')}" if e.image else None
            } for e in exercises]

            return _http_success_response(exercise_list, "Exercises retrieved successfully", 200)

        except AccessDenied as e:
            return _http_error_response(str(e), 401)  # Unauthorized
        except Exception as e:
            _logger.error(f"Error retrieving exercises: {str(e)}")
            return _http_error_response("Internal Server Error", 500)
