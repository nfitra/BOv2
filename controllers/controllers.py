# -*- coding: utf-8 -*-
# from odoo import http


# class BookingOrderFitra(http.Controller):
#     @http.route('/booking_order_fitra/booking_order_fitra/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/booking_order_fitra/booking_order_fitra/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('booking_order_fitra.listing', {
#             'root': '/booking_order_fitra/booking_order_fitra',
#             'objects': http.request.env['booking_order_fitra.booking_order_fitra'].search([]),
#         })

#     @http.route('/booking_order_fitra/booking_order_fitra/objects/<model("booking_order_fitra.booking_order_fitra"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('booking_order_fitra.object', {
#             'object': obj
#         })
