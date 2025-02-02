# -*- coding: utf-8 -*-
# from odoo import http


# class Easy-gym(http.Controller):
#     @http.route('/easy-gym/easy-gym', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/easy-gym/easy-gym/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('easy-gym.listing', {
#             'root': '/easy-gym/easy-gym',
#             'objects': http.request.env['easy-gym.easy-gym'].search([]),
#         })

#     @http.route('/easy-gym/easy-gym/objects/<model("easy-gym.easy-gym"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('easy-gym.object', {
#             'object': obj
#         })

