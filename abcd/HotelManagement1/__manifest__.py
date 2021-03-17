{
	'name': "Hotel Management",

	'summary': "Hotel-Management-System",

	'author': "Rutvik Shah",

	'version':'1.0',

    'website': 'abc@gmail.com',

	'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/hotel_room_views.xml',
        'views/room_type_views.xml',
        'views/hotel_registration_views.xml',
        'views/customer_guest_views.xml',
        'views/customer_document_views.xml',
        'views/hotel_inquiry_views.xml'
    ],

    'demo' : [ ],
 

    'installable':True,

    'application':True,

}