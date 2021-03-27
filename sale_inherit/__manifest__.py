# -*- coding: utf-8 -*-
{
    'name': "Inherit Sale",

    'author': "Brainvire",
    'website': "http://www.yourcompany.com",
   
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','sale'],

    'data': [
        'security/security_group.xml',
        'views/sale_inherit_limit_views.xml',
        'views/sale_inherit_state.xml',
        'views/approvr_pending_view.xml',
    ],
 
}
