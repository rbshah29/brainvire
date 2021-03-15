from odoo import models,fields,api
from odoo.exceptions import ValidationError,Warning

class RoomInquiry(models.TransientModel):
	_name = "room.inquiry"

	room_ids = fields.Many2many('hotel.room') 
	# regi = fields.Many2many('hotel.registration')
