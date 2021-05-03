{
	'name': "Data",

	'summary': "Employee Detail",

	'author': "Rutvik Shah",

	'version':'1.0',

    'website': 'abc@gmail.com',

	'depends': ['sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/employee_views.xml',
    ],

    'demo' : [ ],
 

    'installable':True,

    'application':True,

}