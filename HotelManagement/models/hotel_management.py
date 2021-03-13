from odoo import models,fields,api
from odoo.exceptions import ValidationError,Warning


class HotelRoom(models.Model):
	_name = 'hotel.room'

	room_no = fields.Integer(required=True)
	room_type = fields.Many2one('room.type',required=True)
	hotel_floor = fields.Selection([('a', '1'),
                    ('b', '2'),
                    ('c', '3')])
	room_size = fields.Integer()

	state = fields.Selection([
		('draft', 'Draft'),
            ('process', 'Process')],default='draft')

	def process_progressbar(self):
			self.write({
			'state':'process'
			})


class RoomType(models.Model):
	_name = 'room.type'
	_rec_name = 'type'

	type = fields.Char()

class HotelRegistration(models.Model):
	_name = "hotel.registration"
	registration_sequence = fields.Char(string="Registration no.", readonly=True, required=True, copy=False, default='New')
	# registration_sequence = fields.Integer()
	customer_name = fields.Char(required=True)
	mobile = fields.Integer()
	date_of_birth = fields.Date()
	document = fields.One2many('customer.document','regi',required=True)
	guest_list = fields.One2many('customer.guest','registration_guest')


	@api.model
	def create(self, vals):
	   if vals.get('registration_sequence', 'New') == 'New':
	       vals['registration_sequence'] = self.env['ir.sequence'].next_by_code(
	           'self.service') or 'New'
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

	customer = fields.Many2one("res.partner",required=True)
	start_date = fields.Date(required=True)
	end_date = fields.Date(required=True)
	room_type_id = fields.Many2one('room.type',required=True)
	room_size = fields.Integer(required=True)

	def one(self):
		# print("\n\n\n\n\n\nroom not avaiable\n\n\n\n\n")
		inquiry = self.env['hotel.room'].search(['&',('room_type','=',self.room_type_id.id),('room_size','>=',self.room_size)])	

		if inquiry:
			print("______________--------------________________--------------________________-----------_______________")
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
			print("\n\n\n\n\n\n\n\n\n\n------------------------>>>>>>>>>>>>>>>>>>>>>>>>>ERROT>>>>>>>>>>>>>>>>>>>>>>-----------\n\n\n")
			raise ValidationError("ROOM NOT AVAIABLE")
		

  #get_record=self.env['hotel.room'].search([('date_from','>=',self.date_to),('date_from','<=',self.date_to)])
