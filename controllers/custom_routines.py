import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied, ValidationError
from .auth import JWTAuth
from ._helpers import _success_response, _error_response, _http_error_response, _http_success_response

_logger = logging.getLogger(__name__)

class CustomRoutinesController(http.Controller):
    @http.route('/api/easy_apps/gym/custom_routines/new', type='jsonrpc', auth="none", methods=['POST'])
    def create_custom_routine(self, **kwargs):
        """Create a new custom routine for the authenticated user without exercises"""
        try:
            user = JWTAuth.authenticate_request()

            name = kwargs.get('name')

            if not name:
                raise ValidationError("Routine name is required")

            custom_routine = request.env['easy_gym.custom_routines'].sudo().create({
                'name': name,
                'user_id': user.get('user_id'),
                'routine_exercise_ids':  []
            })

            return _success_response({'id': custom_routine.id}, "Custom routine created successfully")

        except (AccessDenied, ValidationError) as e:
            return _error_response(str(e), 400)
        except Exception as e:
            _logger.error(f"Error creating custom routine: {str(e)}")
            return _error_response("Internal Server Error", 500)

    @http.route('/api/easy_apps/gym/custom_routines/add_exercises', type='jsonrpc', auth="none", methods=['POST'])
    def add_exercises_to_routine(self, **kwargs):
        """Add exercises to an existing custom routine"""
        try:
            user = JWTAuth.authenticate_request()
            exercises = kwargs.get('exercises')
            if not exercises:
                raise ValidationError("Exercises are required")
            # Validate if the routine belongs to the user
            user_id = user.get('user_id')
            routine_ids = list(set(exercise.get('routine_id') for exercise in exercises if exercise.get('routine_id')))
            if len(routine_ids) > 1:
                raise AccessDenied('All exercises must belong to the same routine')
            if not routine_ids:
                raise ValidationError('No valid routine_id found in exercises')
            routine_info = request.env['easy_gym.custom_routines'].sudo().search([('id', '=', routine_ids[0])], limit=1)
            if not routine_info:
                raise AccessDenied('Routine does not exist')
            if routine_info.user_id.id != user_id:
                raise AccessDenied('Routine does not belong to the user')

            # add the exercises to the routine
            added_exercises = []
            for exercise in exercises:
                exercise_id = exercise.get('exercise_id')
                custom_exercise_id = exercise.get('custom_exercise_id')

                # Ensure at least one of exercise_id or custom_exercise_id is present
                if not exercise_id and not custom_exercise_id:
                    raise ValidationError("Each entry must have either 'exercise_id' or 'custom_exercise_id'")

                added_exercise = request.env['easy_gym.routine_exercise'].sudo().create({
                    'routine_id': routine_ids[0],
                    'exercise_id': exercise_id,
                    'custom_exercise_id': custom_exercise_id,
                    'order': exercise.get('order', 0),  # Default order to 0 if missing
                    'superserie_group': exercise.get('superserie_group', 0),
                })
                added_exercises.append(added_exercise.id)

            return _success_response({'added_exercises': added_exercises}, "Exercises added to routine successfully")

        except (AccessDenied, ValidationError) as e:
            return _error_response(str(e), 400)
        except Exception as e:
            _logger.error(f"Error adding exercises to routine: {str(e)}")
            return _error_response("Internal Server Error", 500)


    @http.route('/api/easy_apps/gym/custom_routines', type='http', auth="none", methods=['GET'])
    def get_custom_routines(self, **kwargs):
        """Retrieve all custom routines for the authenticated user"""
        try:
            user = JWTAuth.authenticate_request()
            user_id = user.get('user_id')

            custom_routines = request.env['easy_gym.custom_routines'].sudo().search([('user_id', '=', user_id)])
            routine_list = [{
                'id': r.id,
                'name': r.name,
                'routine_exercise_ids': [e.id for e in r.routine_exercise_ids]
            } for r in custom_routines]

            return _success_response(routine_list, "Custom routines retrieved successfully")

        except AccessDenied as e:
            return _error_response(str(e), 401)
        except Exception as e:
            _logger.error(f"Error retrieving custom routines: {str(e)}")
            return _error_response("Internal Server Error", 500)


    @http.route('/api/easy_apps/gym/custom_routines/get_exercises/<int:routine_id>', type='http', auth="none", methods=['GET'], csrf=False)
    def get_exercises_per_routine(self, routine_id, **kwargs):
        """Retrieve all exercises for a given custom routine (protected with JWT)"""
        try:
            #  Authenticate user using JWT
            user = JWTAuth.authenticate_request()
            user_id = user.get('user_id')  # Extract from decoded JWT

            #  Validate if routine exists and belongs to the user
            routine_info = request.env['easy_gym.custom_routines'].sudo().search([('id', '=', routine_id)], limit=1)
            if not routine_info:
                return _http_error_response('Routine does not exist', 400)
            if routine_info.user_id.id != user_id:
                return _http_error_response('Routine does not belong to the user', 403)

            #  Retrieve all exercises related to the routine
            exercises = [{
                'id': exercise.id,
                'routine_id': exercise.routine_id.id,
                'exercise_id': exercise.exercise_id.id if exercise.exercise_id else None,
                'custom_exercise_id': exercise.custom_exercise_id.id if exercise.custom_exercise_id else None,
                'order': exercise.order,
                'superserie_group': exercise.superserie_group,
            } for exercise in routine_info.routine_exercise_ids]

            #  Return HTTP JSON success response
            return _http_success_response(exercises, "Exercises retrieved successfully", 200)

        except AccessDenied as e:
            return _http_error_response(str(e), 401)

        except Exception as e:
            _logger.error(f"Error retrieving custom routines: {str(e)}")
            return _http_error_response("Internal Server Error", 500)


    @http.route('/api/easy_apps/gym/custom_routines/update', type='jsonrpc', auth="none", methods=['PUT'])
    def update_custom_routine(self, **kwargs):
        """Update a custom routine"""
        try:
            user = JWTAuth.authenticate_request()
            user_id = user.get('user_id')
            routine_id = kwargs.get('id')
            routine = request.env['easy_gym.custom_routines'].sudo().browse(routine_id)

            if not routine.exists() or routine.user_id.id != user_id:
                return _error_response("Routine not found or unauthorized", 400)

            update_data = {}
            if 'name' in kwargs:
                update_data['name'] = kwargs['name']
            if 'routine_exercise_ids' in kwargs:
                update_data['routine_exercise_ids'] = [(6, 0, kwargs['routine_exercise_ids'])] # receives the list complete of exercises, if no in this list will be removed.

            routine.sudo().write(update_data)

            return _success_response({'id': routine.id}, "Routine updated successfully")

        except AccessDenied as e:
            return _error_response(str(e), 401)
        except Exception as e:
            _logger.error(f"Error updating routine: {str(e)}")
            return _error_response("Internal Server Error", 500)

    http.route('/api/easy_apps/gym/custom_routines/update_exercises', type='jsonrpc', auth="none", methods=['PUT'])
    def update_exercise_routine(self, **kwargs):
        """Update a custom routine"""
        try:
            user = JWTAuth.authenticate_request()
            user_id = user.get('user_id')
            routine_id = kwargs.get('routine_id')
            custom_exercise_id = kwargs.get('id')
            routine = request.env['easy_gym.custom_routines'].sudo().browse(routine_id)
            if not routine.exists():
                return _error_response("Routine not found", 404)
            if routine.user_id.id != user_id:
                return _error_response("Unauthorized", 401)

            custom_exercise= request.env['easy_gym.routine_exercise'].sudo().search([('id', '=', custom_exercise_id)], limit=1)
            if not custom_exercise:
                return _error_response('Cant find exercise on DB', 400)
            update_data = {}
            if 'exercise_id' in kwargs:
                update_data['exercise_id'] = kwargs['exercise_id']
            if 'custom_exercise_id' in kwargs:
                update_data['custom_exercise_id'] = kwargs['custom_exercise_id']
            if 'order' in kwargs:
                update_data['order'] = kwargs['order']
            if 'superserie_group' in kwargs:
                update_data['superserie_group'] = kwargs['superserie_group']
            
            custom_exercise.sudo().write(update_data)

            return _success_response({'id': routine.id}, "Routine updated successfully")

        except AccessDenied as e:
            return _error_response(str(e), 401)
        except Exception as e:
            _logger.error(f"Error updating routine: {str(e)}")
            return _error_response("Internal Server Error", 500)

    # @http.route('/api/easy_apps/gym/custom_routines/<int:routine_id>', type='jsonrpc', auth="none", methods=['DELETE'])
    # def delete_custom_routine(self, routine_id, **kwargs):
    #     """Delete a custom routine"""
    #     try:
    #         user = JWTAuth.authenticate_request()
    #         user_id = user.get('user_id')

    #         routine = request.env['easy_gym.custom_routines'].sudo().browse(routine_id)

    #         if not routine.exists() or routine.user_id.id != user_id:
    #             return _error_response("Routine not found or unauthorized", 400)

    #         routine.sudo().unlink()

    #         return _success_response({'id': routine_id}, "Routine deleted successfully")

    #     except AccessDenied as e:
    #         return _error_response(str(e), 401)
    #     except Exception as e:
    #         _logger.error(f"Error deleting routine: {str(e)}")
    #         return _error_response("Internal Server Error", 500)
