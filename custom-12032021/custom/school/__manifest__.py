{
	'name': "School",

	'summary': "School-management-system",

	'author': "Rutvik Shah",

	'version':'1.0',

    'website': 'abc@gmail.com',

	'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/recuirment_views.xml',
        'views/student_views.xml',
        'views/document_views.xml',
        'views/std_views.xml',
    ],

    'demo' : [ ],
 

    'installable':True,

    'application':True,

}