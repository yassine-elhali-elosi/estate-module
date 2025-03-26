{
    'name': 'Estate Data Module',
    'depends': ['base', 'base_import_module'],
    'data': [
        'models/estate_property.xml',
        'security/ir.model.access.csv',
        'views/property_view.xml'
    ],
    'application': True
}