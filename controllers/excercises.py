import logging
from odoo import http
from odoo.http import request, Response
from auth import JWTAuth
from _helpers import _success_response, _error_response
# _logger = logging.getLogger(__name__)

class ExercisesController(http.Controller):

    @http.route('/api/easy_apps/gym/exercises', type='jsonrpc', auth="none", methods=['POST'])
    def get_exercises(self, **kwargs):
        """Retrieve a list of exercises"""
        try:
            JWTAuth.authenticate()  # Verify JWT authentication

            exercises = request.env['easy_gym.exercises'].sudo().search([])

            exercise_list = [{
                'id': e.id, 
                'name': e.name, 
                'focus_area_id': e.focus_area_id.id if e.focus_area_id else None,
                'image': f"data:image/png;base64,{e.image.decode('utf-8')}" if e.image else None
            } for e in exercises]

            return _success_response(exercise_list, "Exercises retrieved successfully")

        except Exception as e:
            return _error_response(str(e), 500)
