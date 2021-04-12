# -*- coding: utf-8 -*-
{
    'name': "Doctor Appointment",

    'author': "Brainvire",
    'website': "http://www.yourcompany.com",
   
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','sale','website'],

    'data': [
        'security/ir.model.access.csv',
        'views/doctor_appoinment_views.xml',
        'views/form_appointment_website_template.xml',
        'views/thank_you_template.xml'
    ],
 
}
