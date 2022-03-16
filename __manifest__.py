# -*- coding: utf-8 -*-
{
    'name': "BOv2",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "nfitra",
    'website': "http://www.hashmicro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management'],

    # always loaded
    'data': [
        'data/seq_saleworkorder.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/service_team.xml',
        'views/booking_order.xml',
        'views/work_order.xml',
        'wizard/cancellation_work_order.xml',
        'wizard/message_check_bo.xml',
        'report/report.xml',
        'report/report_work_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
