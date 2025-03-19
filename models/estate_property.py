from odoo import models, fields
from datetime import timedelta

ORIENTATIONS = [
    ('north', 'North'),
    ('south', 'South'),
    ('east', 'East'),
    ('west', 'West')
]

PROPERTY_STATE = [
    ('new', 'New'),
    ('offer_received', 'Offer received'),
    ('offer_accepted', 'Offer accepted'),
    ('sold', 'Sold'),
    ('canceled', 'Canceled')
]

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "An estate property"

    name = fields.Char('Propertys name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Pstcode')
    date_availability = fields.Date('Aailability', copy=False, default=fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float('Excpected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=ORIENTATIONS
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=PROPERTY_STATE,
        default='new'
    )