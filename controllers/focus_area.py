import logging
from odoo import http
from odoo.http import request, Response
from auth import JWTAuth
from _helpers import _success_response, _error_response
# _logger = logging.getLogger(__name__)

class FocusAreaController(http.Controller):

    @http.route('/api/easy_apps/gym/focus_areas', type='jsonrpc', auth="none", methods=['POST'])
    def get_focus_areas(self, **kwargs):
        """Retrieve a list of focus areas"""
        try:
            JWTAuth.authenticate()  # Verify JWT authentication

            focus_areas = request.env['easy_gym.focus_area'].sudo().search([])

            focus_area_list = [{
                'id': f.id,
                'name': f.name,
                'image': f"data:image/png;base64,{f.image.decode('utf-8')}" if f.image else None
            } for f in focus_areas]

            return _success_response(focus_area_list, "Focus areas retrieved successfully")

        except Exception as e:
            return _error_response(str(e), 500)
