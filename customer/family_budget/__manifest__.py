# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Family Budget',
    'version': '1.0',
    'author': 'Hamoud Hmd',
    'summary': 'Family Budget Management software',
    'sequence': -111,
    'description': """ Family Budget Management software """,
    'category': 'Productivity',
    'website': 'https://www.odoo.com',
    'depends': [
        'mail'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/member_view.xml',
        'views/contribution_view.xml',
        'views/withdraw_view.xml',
        'views/budget_view.xml',
        'views/dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'family_budget/static/src/scss/style.scss',
            'family_budget/static/lib/bootstrap-toggle-master/css/bootstrap-toggle.min.css',
            'family_budget/static/src/js/family_dashboard.js',
            'family_budget/static/lib/Chart.bundle.js',
            'family_budget/static/lib/Chart.bundle.min.js',
            'family_budget/static/lib/Chart.min.js',
            'family_budget/static/lib/Chart.js',
            'family_budget/static/lib/bootstrap-toggle-master/js/bootstrap-toggle.min.js',
        ],
        'web.assets_qweb': [
            'family_budget/static/src/xml/template.xml',
        ],
    },
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
