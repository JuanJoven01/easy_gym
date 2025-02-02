import jwt
import datetime
import logging
from odoo import http
from odoo.http import request, Response

# _logger = logging.getLogger(__name__)

class JWTAuth:
    """Middleware for handling JWT authentication"""

    @staticmethod
    def get_secret_key():
        """Fetch secret key from Odoo system parameters"""
        return request.env['ir.config_parameter'].sudo().get_param('easy_apps_secret_key', 'default_secret')

    @staticmethod
    def generate_token(user):
        """Generate JWT token for authentication"""
        payload = {
            'user_id': user.id,
            'login': user.login,
            'exp': datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
        }
        return jwt.encode(payload, JWTAuth.get_secret_key(), algorithm='HS256')

    @staticmethod
    def decode_token(token):
        """Decode JWT token"""
        try:
            return jwt.decode(token, JWTAuth.get_secret_key(), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return {'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}

    @staticmethod
    def authenticate_request():
        """Middleware to verify JWT token in protected endpoints"""
        token = request.httprequest.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return {'error': 'Missing or invalid token'}
        token = token.split(' ')[1]
        return JWTAuth.decode_token(token)


class JWTAuthController(http.Controller):
    @http.route('/api/easy_apps/gym/auth', type='jsonrpc', auth='public', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        """
        Authenticate user and return JWT token.
        """
        login = kwargs.get('login')
        password = kwargs.get('password')

        if not login or not password:
            return {"error": "Missing login or password"}

        # Search for user in Odoo
        user = request.env['res.users'].sudo().search([('login', '=', login)], limit=1)
        
        if not user or not user._check_password(password):
            return {"error": "Invalid credentials"}

        # Generate JWT token
        token = JWTAuth.generate_token(user)

        return {'token': token, 'user_id': user.id, 'login': user.login}

