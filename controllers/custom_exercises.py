import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied, ValidationError
from .auth import JWTAuth
from ._helpers import _success_response, _error_response, _http_success_response, _http_error_response

_logger = logging.getLogger(__name__)

class CustomExercisesController(http.Controller):

    @http.route('/api/easy_apps/gym/custom_exercises', type='jsonrpc', auth="none", methods=['POST'])
    def create_custom_exercise(self, **kwargs):
        """Create a new custom exercise for the authenticated user"""
        try:
            user = JWTAuth.authenticate_request()  # Authenticate user

            name = kwargs.get('name')
            focus_area_id = kwargs.get('focus_area_id')
            image = kwargs.get('image', None)  # Optional image

            if not name or not focus_area_id:
                raise ValidationError("Name and Focus Area are required")

            custom_exercise = request.env['easy_gym.custom_exercises'].sudo().create({
                'name': name,
                'user_id': user.get('user_id'),  # Associate exercise with the user
                'focus_area_id': focus_area_id,
                'image': image
            })

            return _success_response({'id': custom_exercise.id}, "Custom exercise created successfully")

        except (AccessDenied, ValidationError) as e:
            return _error_response(str(e), 400)
        except Exception as e:
            _logger.error(f"Error creating custom exercise: {str(e)}")
            return _error_response("Internal Server Error", 500)

    @http.route('/api/easy_apps/gym/custom_exercises', type='http', auth="none", methods=['GET'], csrf=False)
    def get_custom_exercises(self, **kwargs):
        """Retrieve all custom exercises for the authenticated user"""
        try:
            #  Authenticate user using JWT
            user = JWTAuth.authenticate_request()
            user_id = user.get('user_id')

            #  Fetch custom exercises for the user
            custom_exercises = request.env['easy_gym.custom_exercises'].sudo().search([('user_id', '=', user_id)])

            #  Format response data
            exercises_list = [{
                'id': e.id,
                'name': e.name,
                'focus_area_id': e.focus_area_id.id if e.focus_area_id else None,
                'image': f"data:image/png;base64,{e.image.decode('utf-8')}" if e.image else None
            } for e in custom_exercises]

            return _http_success_response(exercises_list, "Custom exercises retrieved successfully", 200)

        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            _logger.error(f"Error retrieving custom exercises: {str(e)}")
            return _http_error_response("Internal Server Error", 500)

    
    @http.route('/api/easy_apps/gym/custom_exercises/<int:exercise_id>', type='http', auth="none", methods=['GET'], csrf=False)
    def get_custom_exercise(self, exercise_id, **kwargs):
        """Retrieve a specific custom exercise by ID for the authenticated user"""
        try:
            #  Authenticate user using JWT
            user = JWTAuth.authenticate_request()
            user_id = user.get('user_id')

            #  Fetch custom exercise
            custom_exercise = request.env['easy_gym.custom_exercises'].sudo().browse(exercise_id)

            #  Validate if the custom exercise exists and belongs to the user
            if not custom_exercise.exists() or custom_exercise.user_id.id != user_id:
                return _http_error_response("Custom exercise not found or unauthorized", 404)

            #  Format response data
            exercise_data = {
                'id': custom_exercise.id,
                'name': custom_exercise.name,
                'focus_area_id': custom_exercise.focus_area_id.id if custom_exercise.focus_area_id else None,
                'image': f"data:image/png;base64,{custom_exercise.image.decode('utf-8')}" if custom_exercise.image else None
            }

            return _http_success_response(exercise_data, "Custom exercise retrieved successfully", 200)

        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            _logger.error(f"Error retrieving custom exercise: {str(e)}")
            return _http_error_response("Internal Server Error", 500)


    @http.route('/api/easy_apps/gym/custom_exercises/<int:exercise_id>', type='jsonrpc', auth="none", methods=['PUT'])
    def update_custom_exercise(self, exercise_id, **kwargs):
        """Update a custom exercise by ID for the authenticated user"""
        try:
            user = JWTAuth.authenticate_request()  # Authenticate user
            user_id = user.get('user_id')

            custom_exercise = request.env['easy_gym.custom_exercises'].sudo().browse(exercise_id)

            if not custom_exercise.exists() or custom_exercise.user_id.id != user_id:
                return _error_response("Custom exercise not found or unauthorized", 404)

            update_data = {}
            if 'name' in kwargs:
                update_data['name'] = kwargs['name']
            if 'focus_area_id' in kwargs:
                update_data['focus_area_id'] = kwargs['focus_area_id']
            if 'image' in kwargs:
                update_data['image'] = kwargs['image']

            custom_exercise.sudo().write(update_data)

            return _success_response({'id': custom_exercise.id}, "Custom exercise updated successfully")

        except AccessDenied as e:
            return _error_response(str(e), 401)
        except Exception as e:
            _logger.error(f"Error updating custom exercise: {str(e)}")
            return _error_response("Internal Server Error", 500)

    @http.route('/api/easy_apps/gym/custom_exercises/<int:exercise_id>', type='jsonrpc', auth="none", methods=['DELETE'])
    def delete_custom_exercise(self, exercise_id, **kwargs):
        """Delete a custom exercise by ID for the authenticated user"""
        try:
            user = JWTAuth.authenticate_request()  # Authenticate user
            user_id = user.get('user_id')

            custom_exercise = request.env['easy_gym.custom_exercises'].sudo().browse(exercise_id)

            if not custom_exercise.exists() or custom_exercise.user_id.id != user_id:
                return _error_response("Custom exercise not found or unauthorized", 404)

            custom_exercise.sudo().unlink()

            return _success_response({'id': exercise_id}, "Custom exercise deleted successfully")

        except AccessDenied as e:
            return _error_response(str(e), 401)
        except Exception as e:
            _logger.error(f"Error deleting custom exercise: {str(e)}")
            return _error_response("Internal Server Error", 500)
