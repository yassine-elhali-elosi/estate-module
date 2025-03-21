{
    'name': 'Real Estate',
    'depends': ['base'],
    'data': [
        'views/estate_property_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_types_view.xml',
        'views/res_users_view.xml',
        'security/ir.model.access.csv',
    ],
    'application': True
}