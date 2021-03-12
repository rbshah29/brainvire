{
	'name': "Product",

	'summary': "Product Detail",

	'author': "Rutvik Shah",

	'version':'1.0',

    'website': 'abc@gmail.com',

	'depends': ['sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_brand.xml',
        'views/inherit.xml',
        'views/inherit_sale.xml',
    

    ],

    'demo' : [ ],
 

    'installable':True,

    'application':True,

}