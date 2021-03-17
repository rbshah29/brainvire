from odoo import models,fields,api
from odoo.exceptions import ValidationError,Warning
from lxml import etree

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
    room_regi = fields.Many2one('hotel.registration')
    
    state = fields.Selection([
        ('draft', 'Draft'),
            ('allocated', 'Allocated')],default='draft')

    #to display room_no , room_type , state together:- using name_get method
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s---%s---%s' % (rec.room_no,rec.room_type.type_name,rec.state)))

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
    customer_name = fields.Many2one('res.partner')
    mobile = fields.Integer()
    date_of_birth = fields.Date()

    #we can use either this for customer and guest  
    #1
    room_ids = fields.One2many('customer.guest.line','regi_id')
    #2
    room_regi_ids = fields.Many2one('hotel.room' , domain=[('state','=','draft')])

    document = fields.One2many('customer.document','regi',required=True)

    guest_list = fields.One2many('customer.guest','registration_guest')

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    #works when save button is clickes(overwrite save button)
    #function to get sequence number automatically
    @api.model
    def create(self, vals):
       if vals.get('registration_sequence', 'New') == 'New':
           vals['registration_sequence'] = self.env['ir.sequence'].next_by_code(
               'self.service') or 'New'

       # to make state of specific room allocated when save is pressed    
       # val = {'state':'allocated'}
       # room_allocate = self.env['hotel.room'].search([('id', '=', vals['room_regi_ids'])])
       # for i in room_allocate:
       #      i.write(val)

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



    #function for button 
    def search_one(self):
        #to search requirment from other object
        filtered = self.env['hotel.room'].search([('state','=','draft'),('room_type','=',self.room_type_id.id),
            ('room_size','>',self.room_size)])
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

        #if these condition are true then ir will return anything given             
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
             'view_id': self.env.ref("HotelManagement.regi_form").id,
             'target': 'new'
         }

        else:
            print("___--------___________---------____________--------___________----------________---------_______")
            raise ValidationError("Room not AVAIABLE")


class GuestLine(models.Model):
    _name = 'customer.guest.line'

    #m2m field connected to customer guest to get list of guest 
    guest_ids = fields.Many2many("customer.guest",required=True)
    #m2o field created just for o2m in registration field
    regi_id = fields.Many2one('hotel.registration')
    #m2o field connecting hotel rooms
    room_id = fields.Many2one('hotel.room')
