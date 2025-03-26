{
    'name': 'Estate Data Module',
    'depends': ['base', 'base_import_module'],
    'data': [
        'models/estate_property.xml',
        'models/estate_property_type.xml',
        'views/estate_property_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_menus.xml',
        'security/ir.model.access.csv',
    ],
    'application': True
}