from odoo import models, fields

STATUS = [
    ('accepted', 'Accepted'),
    ('refused', 'Refused'),
]

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate property offer"

    price = fields.Float('Price', required=True)
    status = fields.Selection(
        string='Status',
        selection=STATUS,
        copy=False
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True
    )