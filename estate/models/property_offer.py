from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError

STATUS = [
    ('accepted', 'Accepted'),
    ('refused', 'Refused'),
]

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate property offer"
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price should be strictly positive')
    ]
    _order = "price desc"

    price = fields.Float('Price')
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
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        string='Property type',
        store=True
    )

    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Datetime.from_string(record.create_date)
                record.date_deadline = create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        if self.date_deadline:
            self.validity = (self.date_deadline - fields.Date.today()).days
        else:
            self.validity = 0

    def accept_offer(self):
        for record in self:
            existing_accepted_offer = self.search([
                ('status', '=', 'accepted'),
                ('id', '!=', record.id),
            ], limit=1)

            if existing_accepted_offer:
                raise UserError('Another offer has already been accepted')
            
            if record.status != 'accepted':
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
                record.property_id.state = 'offer_accepted'
            else:
                raise UserError('This offer has already been accepted')

        return True
    
    def refuse_offer(self):
        for record in self:
            if record.status != 'refused':
                record.status = 'refused'
                if record.property_id.state != 'new':
                    record.property_id.selling_price = 0
                    record.property_id.buyer = None
            else:
                raise UserError('This offer has already been refused')
            
    @api.model
    def create(self, values):
        if 'property_id' in values and 'price' in values:
            existing_offer = self.search([
                ('property_id', '=', values['property_id']),
                ('price', '>=', values['price'])
            ], limit=1)

            if existing_offer:
                raise UserError('You cannot create an offer with a price lower than an existing one')

            property_record = self.env['estate.property'].browse(values['property_id'])
            property_record.state = 'offer_received'
            
        return super(EstatePropertyOffer, self).create(values)