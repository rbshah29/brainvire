from odoo import models,fields,api
from odoo.exceptions import ValidationError,Warning
from odoo.osv import expression

class recuirment(models.Model):
	_name = "recuirment"
	_rec_name = "name"


	Id = fields.Char(string="Number", readonly=True, required=True, copy=False, default='New')
	name = fields.Char(string="Name")
	age = fields.Integer()
	subject = fields.Char(required=True)
	experiance = fields.Float(required=True)
	Demo = fields.Boolean()
	joining_date = fields.Date()
	document_ids = fields.One2many('document','rec_id')
	student_id = fields.One2many("student",'tec_ids', string="Student")
	standard_ids = fields.Many2many("standard")

	# for name search
	@api.model
	def _name_search(self, name , args=None, operator="ilike",limit=100,name_get_uid=None):
		context = self.env.context
		if args is None:
			args = []
		else:
			if context.get('stu'):
				std_ids = self.env['standard']._search([('id',operator,context.get('stu'))],limit=limit)
				print(std_ids)
				domain = [('standard_ids','=',std_ids)]
			else:  
				domain = []
		return self._search(expression.AND([domain,args]),limit=limit)


	#for sequence		
	@api.model
	def create(self, vals):
	   if vals.get('Id', 'New') == 'New':
	       vals['Id'] = self.env['ir.sequence'].next_by_code(
	           'self.service') or 'New'
	   result = super(recuirment, self).create(vals)
	   return result

	state = fields.Selection([
		('draft', 'Draft'),
		('need_demo','Need Demo'),('process','Process'),
            ('done', 'Done'),],default='draft')
	def process_progressbar(self):
			self.write({
			'state':'process'
			})
	def done_progressbar(self):

			self.write({
			'state':'done'
			})
	def demo_progressbar(self):
			self.write({
			'state':'need_demo'
			})

class student(models.Model):
	_name = "student"

	name = fields.Char(required=True)
	DOB = fields.Date(required=True)
	hobbies = fields.Char()
	age = fields.Integer()
	image = fields.Image()
	standard_id = fields.Many2one('standard',required=True)
	tec_ids = fields.Many2one("recuirment", string="Teacher",domain=[("state", "=", "done")])

	@api.onchange('standard_id')
	def abc(self):
		self.tec_ids = None

	state = fields.Selection([
		('draft', 'Draft'),
		('process','Process'),
	        ('done', 'Done'),],default='draft')

	def process_progressbar(self):
			self.write({
			'state':'process'
			})

	def done_progressbar(self):
			
			self.write({
			'state':'done'
			})


class document(models.Model):
	_name = "document"

	document= fields.Binary(required=True)
	name_doc = fields.Char()
	date_doc = fields.Date()
	rec_id = fields.Many2one('recuirment')

	# domain=[("recruitment_id.state", "=", "done")]
	# , domain=[("state", "=", "done")]

class standard(models.Model):
	_name = 'standard'
	_rec_name="std"

	std = fields.Integer()
	stu = fields.Many2one('student','student_id')



