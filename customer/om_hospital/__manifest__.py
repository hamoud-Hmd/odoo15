# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hospital management',
    'version': '1.1',
    'author': 'Hamoud Hmd',
    'summary': 'Hospital management software',
    'sequence': -110,
    'description': """ Hospital management software """,
    'category': 'Productivity',
    'website': 'https://www.odoo.com',
    'depends': [
        'sale',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/create_appointment_view.xml',
        'views/patient_view.xml',
        'views/kid_view.xml',
        'views/patient_gender_view.xml',
        'views/appointment_view.xml',
        'views/doctor_view.xml',
        'views/sale.xml',

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
