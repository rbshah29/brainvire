from odoo import models, fields, api


class sale_inherit(models.TransientModel):
    _inherit = "res.config.settings"

    set_limit = fields.Float(config_parameter="sale_inherit.set_limit" ,string="Set Limit")

    @api.model
    def get_values(self):
        res = super(sale_inherit, self).get_values()
        res['set_limit'] = (self.env['ir.config_parameter'].sudo().get_param('sales_inherit.set_limit',
                                                                               default=0))
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('sales_inherit.set_limit', self.set_limit)
        super(sale_inherit, self).set_values()



class sale_inherit_state(models.Model):
	_inherit = "sale.order"

	state = fields.Selection(selection_add=[('to_approve', 'To Approve')])
	
	def approve_click(self):
		self.write(
			{
			'state':'sale'
			}
			)


	def action_confirm(self):
		sup = super(sale_inherit_state, self).action_confirm()
		set_limit =  self.env['ir.config_parameter'].sudo().get_param('sale_inherit.set_limit') or False
		if set_limit:
			if float(self.amount_total)>float(set_limit):
				self.write(
				{
				'state':'to_approve'
				}
				)
	
			

