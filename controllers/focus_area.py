import logging
from odoo import http
from odoo.http import request, Response
from .auth import JWTAuth
from ._helpers import _http_error_response, _http_success_response
from odoo.exceptions import AccessDenied

_logger = logging.getLogger(__name__)

class FocusAreaController(http.Controller):
    @http.route('/api/easy_apps/gym/focus_areas', type='http', auth="none", methods=['GET'], csrf=False)
    def get_focus_areas(self, **kwargs):
        """Retrieve a list of focus areas"""
        try:
            #  Authenticate user using JWT
            user = JWTAuth.authenticate_request()

            #  Check if authentication failed
            if 'error' in user:
                return _http_error_response(user['error'], 401)  # Unauthorized

            #  Fetch all focus areas
            focus_areas = request.env['easy_gym.focus_area'].sudo().search([])

            #  Format response data
            focus_area_list = [{
                'id': f.id,
                'name': f.name,
                'image': f"data:image/png;base64,{f.image.decode('utf-8')}" if f.image else None
            } for f in focus_areas]

            return _http_success_response(focus_area_list, "Focus areas retrieved successfully", 200)

        except AccessDenied as e:
            return _http_error_response(str(e), 401)  # Unauthorized
        except Exception as e:
            _logger.error(f"Error retrieving focus areas: {str(e)}")
            return _http_error_response("Internal Server Error", 500)
