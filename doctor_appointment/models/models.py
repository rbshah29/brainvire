from odoo import models,fields,api

class DocAppoinment(models.Model):
	_name = 'web.appointment'
	# name,age,date of birth,email and contact number 
	name = fields.Char(string='Name')
	age = fields.Integer(string='Age')
	dob = fields.Date(string='Date of birth')
	email = fields.Char(string='Email')
	contact_number = fields.Char(string='Contact Number')

