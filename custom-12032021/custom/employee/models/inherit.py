from odoo import models, fields

class SaleOrder(models.Model):

	_inherit = 'sale.order'

	additional = fields.Char(string='Additional Note')