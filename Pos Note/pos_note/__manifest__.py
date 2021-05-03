# -*- coding: utf-8 -*-
{
    'name': "pos_note",

    'author': "My Company",
    
    'website': "http://www.brainvire.com",
    
    'category': 'Point of Sale',
    
    'version': '0.1',
    
    'depends': ['base', 'point_of_sale'],
    
    'qweb': ['static/pos_note_template.xml'],
    
    'data': [
        'views/pos_extend_note.xml',
        'views/pos_note_form.xml',
    ]
}
