{
    'name': 'Real Estate',
    'depends': ['base'],
    'data': [
        'views/property_tag_view.xml',
        'views/property_offer_view.xml',
        'views/property_type_view.xml',
        'views/property_view.xml',
        'views/res_users_view.xml',
        'views/estate_property_menus.xml',
        'security/ir.model.access.csv',
        'data/estate.property.type.csv',
        'data/estate.property_pdf_data_demo.xml',
        'reports/estate_property_reports.xml',
        'security/security.xml'
    ],
    'category': 'Real Estate/Brokerage',
    'application': True
}