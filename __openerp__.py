{
    "name": "Module 1-Academy",
    "version": "1.0",
    "depends": [
        "base",
        "mail",
        "report_webkit",
        "board",
    ],
    "author": "Carlos Navarro",
    "category": "Academic",
    "description": """
OpenAcademy
===========

Este módulo permite la gestión de centros educativos.

Al instalar el módulo se crean los objetos de curso, session y assitente.
""",
    'data': [
        'module1_menu.xml',
        'module1_Dashboard.xml',
        'module1_view.xml',
        'module1_workflow.xml',
        'wizard/module1_wizard_webkit_view.xml',
        'wizard/module1_wizard_aeroo_view.xml',
        'report/report.xml',
        'report/report_aeroo.xml',
        'security/module1_security.xml',
        'security/ir.model.access.csv',
        'data/demo_student.xml'
        #all other data files, except demo data and tests
        ],
    'demo': [
    
    ],
    'test': [
        #files containg tests
    ],
    'installable': True,
    'auto_install': False,

}