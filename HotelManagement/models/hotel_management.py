from odoo import models,fields,api
from odoo.exceptions import ValidationError,Warning
from lxml import etree


class HotelRoom(models.Model):
	_name = 'hotel.room'
	# _rec_name ="room_no"

	room_no = fields.Integer(required=True)
	room_type = fields.Many2one('room.type',required=True)
	hotel_floor = fields.Selection([('a', '1'),
                    ('b', '2'),
                    ('c', '3')])
	room_size = fields.Integer()

	state = fields.Selection([
		('draft', 'Draft'),
            ('allocated', 'Allocated')],default='draft')

	# @api.model
	# def _fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
	# 	res = super(HotelRoom, self)._fields_view_get(view_id=view_id, view_type=view_type,toolbar=toolbar, submenu=False)
	# 	doc = etree.XML(res['arch'])
	# 	for node in self.env['hotel.room'].search([('id', '=', vals['state'])]):
	# 		if node.state == 'allocated':
	# 			node.set('invisible','1')
	# 	res['arch'] = etree.tostring(doc)
	# 	return res


	def name_get(self):
		res = []

		for rec in self:
			res.append((rec.id, '%s---%s---%s' % (rec.room_no,rec.room_type.type_name,rec.state)))

		return res

	def process_progressbar(self):

			self.write({
			'state':'draft'
			})


class RoomType(models.Model):
	_name = 'room.type'
	_rec_name = 'type_name'

	type_name = fields.Char()

class HotelRegistration(models.Model):
	_name = "hotel.registration"
	registration_sequence = fields.Char(string="Registration no.", readonly=True, required=True, copy=False, default='New')
	# room_num = fields.Many2one('hotel.room')
	customer_name = fields.Many2one('res.partner',required=True)
	mobile = fields.Integer()
	date_of_birth = fields.Date()
	room_regi_ids = fields.Many2one('hotel.room' , domain=[('state','=','draft')])
	document = fields.One2many('customer.document','regi',required=True)
	guest_list = fields.One2many('customer.guest','registration_guest')
	start_date = fields.Date('Start Date')
	end_date = fields.Date('End Date')

	


	@api.model
	def create(self, vals):
	   if vals.get('registration_sequence', 'New') == 'New':
	       vals['registration_sequence'] = self.env['ir.sequence'].next_by_code(
	           'self.service') or 'New'


	   val = {'state':'allocated'}
	   room_allocate = self.env['hotel.room'].search([('id', '=', vals['room_regi_ids'])])
	   for i in room_allocate:
	   		i.write(val)


	   result = super(HotelRegistration, self).create(vals)
	   return result
	     


	state = fields.Selection([
		('draft', 'Draft'),
            ('process', 'Process'),('done','Done')],default='draft')

	def process_progressbar(self):
			self.write({
			'state':'process'
			})

	def done_progressbar(self):
			self.write({
			'state':'done'
			})
		
class CustomerGuest(models.Model):
	_name = 'customer.guest'

	name = fields.Char(required=True)
	document_guest = fields.One2many('customer.document','guest',required=True)
	registration_guest = fields.Many2one('hotel.registration')

class CustomerDocument(models.Model):
	_name = "customer.document"

	regi = fields.Many2one('hotel.registration')
	guest = fields.Many2one('customer.guest')
	document = fields.Binary(required=True)
	document_name = fields.Char(required=True)

class RegistrationInquiry(models.TransientModel):
	_name = 'registration.inquiry'

	# customer = fields.Many2one("res.partner",required=True)
	start_date = fields.Date()
	end_date = fields.Date()
	room_type_id = fields.Many2one('room.type',required=True)
	room_size = fields.Integer(required=True)



	def one(self):
	 	inquiry = self.env['hotel.room'].search(['&',('room_type','=',self.room_type_id.id),('room_size','>=',self.room_size),('state','=','draft')])	
	 
	 	if inquiry:
	 		print("---------------->>>>>>>>>>>>----AVAIABLE-------<<<<<<<<<<-------------")
	 		return {
             'name': 'inquiry_registration_form',
             'res_model': 'hotel.registration',
             'type': 'ir.actions.act_window',
             'context': {},
             'view_mode': 'form',
             'view_type': 'form',
             'view_id': self.env.ref("HotelManagement.regi_form").id,
             # 'domain'=[]
             'target': 'new'
         }
	 	else:
	 		print("\n\n\n\n\n\n\n\n\n\n------------------------>>>>>>>>>>>>>>>>>>>>>>>>>ERROR>>>>>>>>>>>>>>>>>>>>>>-----------\n\n\n")
	 		raise ValidationError("ROOM NOT AVAIABLE")


