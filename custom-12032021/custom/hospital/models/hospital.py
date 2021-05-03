from odoo import models,fields,api
from odoo.exceptions import ValidationError,Warning

class hospital(models.Model):
	_name = "hospital"

	name = fields.Char(required=True)
	age = fields.Integer(required=True)
	notes = fields.Text(required=True)
	doctor = fields.Many2one('doctor', string="doctor")
	tablet_id = fields.One2many('tablet_line','patient')
	sub_total = fields.Integer(string="Total" ,compute="_subtotal")
	#use for state field 
	state = fields.Selection([
		('draft', 'Draft'),
            ('done', 'Done'),],default='draft')


  
	#use to change state bar
	def done_progressbar(self):
		for rec in self:
			for ta in rec.tablet_id:
				ta.tab.quantity = ta.tab.quantity - ta.qty
			self.write({
			'state':'done'
			})
			#orm method
	def method(self):
		for rec in self:
			patient = self.env['hospital'].search([]) 
			patient = self.env['hospital'].search([("name","=","rutvik")])
			print("**********************************************************",patient)
			print("========================================")
			patient = self.env['hospital'].search_count([])
			print(patient)
			refe = self.env.ref('hospital.hospital_search')
			print("refe = =  = = = = ", refe)
			browse = self.env['hospital'].browse([1194])
			print("-----------------",browse)
			if browse.exists():
				print("exist")
			else:
				print("dont exist")
		
	#call total form another model using table_id (one2many)
	#gives you grand total of all the item you have selected
	@api.depends('tablet_id.total')
	def _subtotal(self):
		t = 0
		for rec in self:
			for r in rec.tablet_id:
				t += r.total
			rec.sub_total = t


class tablet(models.Model):
	_name = 'tablet'
	_rec_name = 'tab_name'

	tab_name = fields.Char(required=True)
	quantity = fields.Integer(required=True)

	#this will raise an pop-up notification along with name of medicine 
	@api.constrains('quantity')
	def _check_something(self):
		for record in self:
			if record.quantity < 0:
				raise ValidationError("%s is not in stock"%record.tab_name)
				



class tablet_line(models.Model):
	_name = 'tablet_line'

	tab = fields.Many2one('tablet',string="Tablet",required="True")
	patient = fields.Many2one('hospital', string="Patient")
	qty = fields.Integer(string='Qty')
	price = fields.Integer(string="Price")
	total = fields.Integer(string="Total")

	#gives you total onchange of you quantity and price
	@api.onchange('qty','price')
	def _total(self):
		for rec in self:
			rec.total = rec.price*rec.qty


class doctor(models.Model):
	_name = "doctor"

	name = fields.Char(required=True)
	age = fields.Integer()
	patient= fields.One2many('hospital','doctor')
	# patient_id = fields.Many2one('hospital')	
	def method1(self):
		for ref in self:
			val={
			'name':'rama'
			}
			#using create method
			crr = self.env['doctor'].create(val)
			#gaining id for above variable
			print("---------------------------------------------------------------------------",crr,crr.id)
			#using browse function
			record_update = self.env['doctor'].browse(31)
			#using write method
			if record_update.exists():
				vals = {
					'age':54
				}
				record_update.write(vals)
				#using copy method
			record_copy = self.env['doctor'].browse(33)
			record_copy.copy()
			#using unlink method
			record_copy = self.env['doctor'].browse(35)
			record_copy.unlink()