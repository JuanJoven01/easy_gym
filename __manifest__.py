# -*- coding: utf-8 -*-
{
    'name': "easy-gym",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/focus_area_views.xml',
        'views/exercises_views.xml',
        'views/custom_routines_views.xml',
        'views/custom_exercises_views.xml',
        'views/exercises_records_views.xml', # Since here now saw
        'views/routine_exercises_views.xml',
        'views/routines_records_views.xml',
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

