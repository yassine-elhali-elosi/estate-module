from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

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
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The property expected price should be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The property selling price should be positive')
    ]
    _order = "id desc"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability', copy=False, default=fields.Date.today() + timedelta(days=90))
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

    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property type'
    )
    buyer = fields.Many2one(
        'res.partner',
        string='Buyer'
    )
    salesperson = fields.Many2one(
        'res.users',
        string='Salesperson'
        #default=lambda self: self.env.user
    )

    tag_ids = fields.Many2many( # relation name
        'estate.property.tag',
        string='Tags'
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    total_area = fields.Float(compute='_compute_total_area')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float('Best Offer', compute='_compute_best_price')

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def cancel_property(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise UserError('You cannot cancel a sold property')
                
        return True
    
    def sold_property(self):
        for record in self:
            if record.state != 'offer_accepted':
                raise UserError('You cannot sell a property that does not have an accepted offer')
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError('You cannot sell a canceled property')

        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError('The selling price must be at least 90% of the expected price.')
    
    @api.ondelete(at_uninstall=False)
    def _check_property_state(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError('You cannot delete a property that is not new or canceled')