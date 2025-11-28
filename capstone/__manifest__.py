# -*- coding: utf-8 -*-
{
    'name': "Capstone Project",
    'summary': """
        Capstone Capstone PT Demo""",
    'description': """
        Interfacing Capstone
    """,

    'author': "Saya",
    'website': "https://www.demo.co.id",

    'category': 'Inventory',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'views/form_dokumen.xml',
        'security/ir.model.access.csv',
        'wizard/laporan_penyelesaian_views.xml',
    ],
    
    'application': True,
    
    'license': 'LGPL-3',
}
