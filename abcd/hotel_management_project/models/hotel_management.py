from odoo import models,fields,api
from odoo.exceptions import ValidationError,Warning
from lxml import etree
import datetime


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
    
    state = fields.Selection([
        ('draft', 'Draft'),
            ('allocated', 'Allocated')],default='draft')

    #to display room_no , room_type , state together:- using name_get method
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s---%s' % (rec.room_no,rec.room_type.type_name)))

        return res


    def process_progressbar(self):

            self.write({
            'state':'draft'
            })

# table for room type
class RoomType(models.Model):
    _name = 'room.type'
    _rec_name = 'type_name'

    type_name = fields.Char()

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

    # creat_date = fields.Date(string='Date of registration', default=datetime.datetime.today())

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


    def cancle_method(self):
        print("----->>>>>>>>inside")
        previous_date = datetime.datetime.today() - datetime.timedelta(days=3)  
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
    startDate = fields.Date(required=True)
    endDate = fields.Date(required=True)
    #m2o field connecting room types
    room_type_id = fields.Many2one('room.type',required=True)
    room_size = fields.Integer(required=True, placeholder="For how many person")
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


class methodabstract(models.AbstractModel):
    _name = 'report.hotel_management_project.action_report_registration'
    _description = 'calling abstract class'

    def _one_method(self,doc):
        return 'rutvik'

    @api.model
    def _get_report_values(self, docids, data=None):
         docs = self.env['hotel.registration'].browse(docids)
         print("\n\n\n\n------------inside>>>>>>>>>>>\n\n\n\n\n",docs)
         return {
            'doc_ids': docs.ids,
            'doc_model': 'hotel.registration',
            'docs': docs,
            'data':data,
            'one_method': self._one_method
        }


#class for Mail System
    