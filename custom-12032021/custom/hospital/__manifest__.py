{
	'name': "Hospital",

	'summary': "Hospital Detail",

	'author': "Rutvik Shah",

	'version':'1.0',

    'website': 'abc@gmail.com',

	'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/hospital_views.xml',
        'views/doctor_views.xml',
        'views/tablet_views.xml',
        'views/line_views.xml',
    ],

    'demo' : [ ],
 

    'installable':True,

    'application':True,

}