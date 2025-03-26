{
    'name': 'Estate Data Module',
    'depends': ['base', 'base_import_module'],
    'data': [
        'security/ir.model.access.csv',
        'models/estate_property.xml',
        'views/estate_property_view.xml',
        'views/estate_property_menus.xml',
    ],
    'application': True
}