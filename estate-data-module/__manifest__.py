{
    'name': 'Estate Data Module',
    'depends': ['base', 'base_import_module'],
    'data': [
        'models/estate_property.xml',
        'views/property_view.xml',
        'security/ir.model.access.csv',
    ],
    'application': True
}