	# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrderNotes(models.Model):
    _inherit = 'pos.order'

    order_note = fields.Text(string="Order Note")

    @api.model
    def _order_fields(self, ui_order):
        print("\n\n\n\n\n\n----------ui----------",ui_order)
        res=super(PosOrderNotes,self)._order_fields(ui_order)
        res['order_note'] = ui_order['order_note'] if ui_order['order_note'] else False
        return res

