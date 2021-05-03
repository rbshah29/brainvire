from odoo import models,fields,api

class Employee(models.Model):
	_name = "employee"

	name = fields.Char(required=True)
	emp_id = fields.Integer(required=True)
	department = fields.Char(required=True)
	image  = fields.Binary()
