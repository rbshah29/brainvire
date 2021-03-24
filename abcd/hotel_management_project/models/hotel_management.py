from odoo import models,fields,api
from odoo.exceptions import ValidationError,Warning
from lxml import etree
import datetime
import xlsxwriter
import io
import base64

# table for hotel room
class HotelRoom(models.Model):
	_name = 'hotel.room'
	room_no = fields.Integer(required=True)
	room_type = fields.Many2one('room.type',required=True)
	many_one = fields.Many2one('registration.inquiry')
	hotel_floor = fields.Selection([('a', '1'),
					('b', '2'),
					('c', '3')])
	room_size = fields.Integer()
	boolean = fields.Boolean()
	room_price = fields.Float(required=True)
	room_regi = fields.Many2one('hotel.registration')
	regi_count = fields.Integer(string="count",compute='count_regi')
	state = fields.Selection([
		('draft', 'Draft'),
			('allocated', 'Allocated')],default='draft')
	#this gives you number of record for that id

	def count_regi(self):
		count = self.env['hotel.registration'].search_count([('room_ids.room_id.room_type','=',self.room_type.id)])
		self.regi_count = count

	#this return you a view in which if record are more than one it will show tree/list view else it will show form view
	def get_smart(self):
		purchase = self.env['hotel.registration'].search([('room_ids.room_id','=',self.id)])
		action = self.env["ir.actions.actions"]._for_xml_id("hotel_management_project.registration_action")
		if self.regi_count > 1:
			action['domain'] = [('room_ids.room_id','=',self.id)]

		elif self.regi_count == 1:
			form_view = [(self.env.ref('hotel_management_project.regi_form').id, 'form')]
			action['views'] = form_view
			action['res_id'] = purchase.id
	  
		return action  

	# def get_smart(self):
	#     self.ensure_one()
	#     if self.regi_count==1:
	#         print("\n\n\n\n----------->")
	#         purchase = self.env['hotel.registration'].search([('room_ids.room_id','=',self.id)])
	#         action = self.env["ir.actions.actions"]._for_xml_id("hotel_management_project.registration_action")
	#         form_view = [(self.env.ref('hotel_management_project.regi_form').id,'')]
	#         action['views'] : form_view
	#         action['res_id'] : purchase.id

	#         return {
	#         "name": "Registration",
	#         'view_mode': 'form',
	#         'view_id':(purchase,'form'),
	#         'view_type': 'form',
	#         "res_model": 'hotel.registration',
	#         "domain": [('room_ids.room_id.room_type','=',self.room_type.id)],
	#         "type": 'ir.actions.act_window',
	#         }
	#     else:  
	#         return {
	#         "name": "Registration",
	#         'view_mode': 'tree,form',
	#         'view_type': 'form',
	#         "res_model": 'hotel.registration',
	#         "domain": [('room_ids.room_id.room_type','=',self.room_type.id)],
	#         "type": 'ir.actions.act_window',
	#         # "readonly":True,
	#         }  


	#to display room_no , room_type , state together:- using name_get method
	def name_get(self):
		res = []
		for rec in self:
			res.append((rec.id, '%s' % (rec.room_type.type_name)))

		return res


	def process_progressbar(self):

			self.write({
			'state':'draft'
			})

# table for room type
class RoomType(models.Model):
	_name = 'room.type'
	_rec_name = 'type_name'

	type_name = fields.Char(required=True)

# table for hotel registration
class HotelRegistration(models.Model):
	_name = "hotel.registration"
	registration_sequence = fields.Char(string="Registration no.", readonly=True, required=True, copy=False, default='New')
	customer_name = fields.Many2one('res.partner',required=True)
	mobile = fields.Integer()
	date_of_birth = fields.Date()
	email_id = fields.Char()
	#we can use either this for customer and guest  
	#1
	room_ids = fields.One2many('customer.guest.line','regi_id',required=True) 
	 #2
	room_regi_ids = fields.Many2one('hotel.room' , domain=[('state','=','draft')])
	document = fields.One2many('customer.document','regi',required=True)
	guest_list = fields.One2many('customer.guest','registration_guest',required=True)
	start_date = fields.Date('Start Date',required=True)
	end_date = fields.Date('End Date',required=True)
	total = fields.Float(readonly=1)


	#to send email 
	def send_regi_email(self):
		print("\n\n\n\n")
		
		self.ensure_one()
		ir_model_data = self.env['ir.model.data']
		try:
			template_id = self.env['ir.model.data'].xmlid_to_res_id('hotel_management_project.email_template_id',
														  raise_if_not_found=False)
			print(template_id, "template_id\n\n\n\n\n")
		except ValueError:
			print("\n\n\n\n value error \n\n\n\n\n\n")
			template_id = False
		try:
			compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
		except ValueError:
			compose_form_id = False


		ctx = {
			'default_model': 'hotel.registration',
			'default_res_id': self.ids[0],
			'default_use_template': bool(template_id),
			'default_template_id': template_id,
			'default_composition_mode': 'comment',
		}
		return {
			'name': ('Compose Email'),
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'mail.compose.message',
			'views': [(compose_form_id, 'form')],
			'view_id': compose_form_id,
			'target': 'new',
			'context': ctx,
		}

		# to call cron job method
	def cancle_method(self):
		print("----->>>>>>>>inside")
		previous_date = datetime.datetime.today() - datetime.timedelta(days=2)  
		cancel_id = self.env["hotel.registration"].search([("state", "=", "process"),('create_date', '<=', previous_date)]) 
		print(cancel_id)
		for reg in cancel_id:
			print("-------------------------------->>>>>>>>>>>inside")
			reg.state = 'cancel'

	#works when save button is clickes(overwrite save button)
	#function to get sequence number automatically      
	@api.model
	def create(self, vals):
	   if vals.get('registration_sequence', 'New') == 'New':
		   vals['registration_sequence'] = self.env['ir.sequence'].next_by_code(
			   'self.service') or 'New'  

	   result = super(HotelRegistration, self).create(vals)
	   return result
		 

	state = fields.Selection([
		('draft', 'Draft'),
			('process', 'Process'),('done','Done'),('cancel','Cancel')],default='draft')

	def process_progressbar(self):
		for rec in self:
			print("_____-----_____________-----________------_________")
			rec.room_ids.room_id.state = 'draft'
			self.write({
			'state':'process'
			})

	def done_progressbar(self):
		for rec in self:
			print("_____-----_____________-----________------_________")
			rec.room_ids.room_id.state = 'allocated'
		self.write({
		'state':'done'
		})
			

# class CrmReport(models.TransientModel):  
#     _name = 'crm.won.lost.report'       
#     start_date = fields.Date('Start Date')    
#     end_date = fields.Date('End Date',default=fields.Date.today)     
#     def print_xls_report(self,cr,uid,ids,context=None):       
#         data= self.read(cr, uid, ids)[0]
#         return {'type': 'ir.actions.report.xml',               
#         'report_name': 'hotel_management_project.report_hotel_xls.xlsx',              
#         'datas': data             
#         }

# table for CustomerGuest
class CustomerGuest(models.Model):
	_name = 'customer.guest'

	name = fields.Char(required=True)

	document_guest = fields.One2many('customer.document','guest',required=True)
	registration_guest = fields.Many2one('hotel.registration')

# table for CustomerDocument   
class CustomerDocument(models.Model):
	_name = "customer.document"

	#m2o created to support o2m
	regi = fields.Many2one('hotel.registration')
	#m2o created to support o2m
	guest = fields.Many2one('customer.guest')
	document = fields.Binary(required=True)
	document_name = fields.Char(required=True)

# table for registration inquiry
class RegistrationInquiry(models.Model):
	_name = 'registration.inquiry'
	
	# m2ofield connecting res.partner
	customer = fields.Many2one("res.partner",required=True)
	startDate = fields.Date()
	endDate = fields.Date()
	#m2o field connecting room types
	room_type_id = fields.Many2one('room.type',required=True)
	room_size = fields.Integer(required=True)
	#o2m connecting hotel room with specific domain
	room_regi = fields.One2many('hotel.room' ,'many_one', domain=[('state','=','draft')])

	total_price = fields.Float(readonly=1,compute='calculate_price')

	@api.onchange('room_regi')
	def calculate_price(self):
		total = 0
		for price in self.room_regi:
			print("------------------\n\n\n\n\n\n\n\n")
			if price.boolean:
				total += price.room_price
		self.write({
			'total_price':total
			})




	#function for button 
	def search_one(self):
		#to search requirment from other object
		filtered = self.env['hotel.room'].search([('state','=','draft'),('room_type','=',self.room_type_id.id),
			('room_size','>=',self.room_size)])
		#i dont know this one
		self.room_regi=[(6,0,[])]
		self.write({'room_regi':filtered})

		return 
	#function for button
	def inquiry_one(self):
		#to check conditoins 

		#to pass only those element which are selected using many2one and one2many field
		#this is use to pass only selected rooms in this module
		res=[]
		for i in self:
			for j in i.room_regi:
				if j.boolean:
					res.append({'room_id':j.id})

		#if these condition are true then it will return anything given             
		inquiry = self.env['hotel.room'].search(['&',('room_type','=',self.room_type_id.id),
			('room_size','>=',self.room_size),('state','=','draft')]) 

		if inquiry:
			#if condition is satisfied it will return a specific view
			return {
			 'name': 'inquiry_registration_form',
			 'res_model': 'hotel.registration',
			 'type': 'ir.actions.act_window',
			 'context': {'default_room_ids':res},
			 'view_mode': 'form',
			 'view_type': 'form',
			 'view_id': self.env.ref("hotel_management_project.regi_form").id,
			 'target': 'new'
		 }

		else:
			print("___--------___________---------____________--------___________----------________---------_______")
			raise ValidationError("Room not AVAIABLE")


class GuestLine(models.Model):
	_name = 'customer.guest.line'

	#m2m field connected to customer guest to get list of guest 
	guest_ids = fields.Many2many("customer.guest")
	#m2o field created just for o2m in registration field
	regi_id = fields.Many2one('hotel.registration')
	#m2o field connecting hotel rooms
	room_id = fields.Many2one('hotel.room')


#this class is for xlsx action using wizard
class WizardReport(models.TransientModel):
	_name = 'wizard.report'

	date_from = fields.Date() 
	date_to = fields.Date()
	

	def generate_xlsx_report_id(self):
		output = io.BytesIO()
		print("touchdown\n\n\n\n\n\n\n")

		data = {
			'start_date': self.date_from.strftime('%d/%b/%Y'),
			'end_date': self.date_to.strftime('%d/%b/%Y'),
		}

		
		workbook = xlsxwriter.Workbook(output, {'in_memory': True})
		worksheet = workbook.add_worksheet()
		merge_format = workbook.add_format({
		'bold': 1,
		'border': 1,
		'align': 'center',
		'valign': 'vcenter',
		# 'fg_color': 'yellow'
		})

		worksheet.set_column(0, 8, 30)
		worksheet.write(0,0,'Date From',merge_format)
		worksheet.write(0,2,'Date To',merge_format)
		
		

		worksheet.write(0,1,data['start_date'])
		# print(data['start_date'])
		worksheet.write(0,3,data['end_date'])
		record = self.env['hotel.registration'].search([('start_date','>=',self.date_from),('start_date','<=',self.date_to)])
		worksheet.write(3,0,'Registration Number',merge_format)
		worksheet.write(3,1,'Customer Name',merge_format)
		worksheet.write(3,2,'Room',merge_format)
		worksheet.write(3,3,'Room No',merge_format)
		row = 4
		col = 0
		# worksheet.merge_range('B10:E10','Merge',merge_format)
		# worksheet.write('B10', 'Hello')
		for i in record:
			worksheet.write(row,col,i.registration_sequence)
			worksheet.write(row,col+1, i.customer_name.name)
			result = i.room_ids
			data=result.room_id

			room_list = []
			room_type_name = []
			for room in i.room_ids.room_id:
				room_list.append(str(room.room_no))

			for room in i.room_ids.room_id:    
				room_type_name.append(str(room.room_type.type_name))
				
			room_all = ', '.join(room_list)
			room_type_all = ', '.join(room_type_name)
			worksheet.write(row,col+2, room_type_all)
			worksheet.write(row,col+3, room_all)
		   
						
			row +=1

		workbook.close()

		output.seek(0)
		attch = self.env['ir.attachment'].create({'name': 'Registrations.xlsx', 'datas': base64.b64encode(output.read())})
		# print(str(self.env['ir.config_parameter'].get_param('web.base.url')) + str(
		#         '/web/content/' + str(attch.id)))
		return {
			'type': 'ir.actions.act_url',
			'url': '/web/content/' + str(attch.id) + '?download=True',
			'target':self
		}
class ImportRoom(models.TransientModel):
	_name = "import.room.wizard"

	upload = fields.Binary(string="Upload File")

	def import_room_id(self):
		# Generating of the excel file to be read by openpyxl
		ab = xlrd.open_workbook(file_contents=base64.decodebytes(self.upload))
		for websheet in ab.sheets():
			room_no:websheet.cell(0,0).value
			room_type:websheet.cell(0,1).value
			hotel_floor:websheet.cell(0,2).value
			room_size:websheet.cell(0,3).value
			room_price:websheet.cell(0,4).value

		self.env['hotel.room'].create({
			'room_no':int(room_no),
			'room_type':int(room_type),
			'hotel_floor':int(hotel_floor),
			'room_size':int(room_size),
			'room_price':int(room_price),			
			})