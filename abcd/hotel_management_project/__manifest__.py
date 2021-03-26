{
	'name': "Hotel Management project",

	'summary': "Hotel-Management-System",

	'author': "Rutvik Shah",

	'version':'1.0',

    'website': 'abc@gmail.com',

	'depends': ['base','mail','sale'],

    'data': [
        'security/ir.model.access.csv',
        'data/cron_data.xml',
        'data/email_views.xml',
        'data/hotel.room.csv',
        'data/registration_sequencr.xml',
        'views/hotel_room_views.xml',
        'views/room_type_views.xml',
        'views/hotel_registration_views.xml',
        'views/customer_guest_views.xml',
        'views/customer_document_views.xml',
        'views/hotel_inquiry_views.xml',
        'report/report_print.xml',
        # 'report/report_xlsx.xml',
        'views/xlsx_report_views.xml',
        'views/import_room_wizard.xml',
        'views/inherit_sale_view.xml',
        'views/sales_wizard_views.xml',
        


    ],

    'demo' : [ ],
 

    'installable':True,

    'application':True,

}