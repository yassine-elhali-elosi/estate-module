from datetime import timedelta
from odoo import models, fields, api

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