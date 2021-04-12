# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request

class Appointment(http.Controller):

    @http.route('/appointment', type='http', auth="user", website=True,)
    def appointment(self,**kw):
        return http.request.render('doctor_appointment.appointment_page_template_id',{})


    @http.route('/appointment_create', type='http', auth="user", website=True, method='POST')
    def appointment_create(self,**kw):
        print("-----------------------\n\n\n\n\n",kw)
        request.env["web.appointment"].sudo().create(kw)
        return request.render("doctor_appointment.thank_you_template",{})