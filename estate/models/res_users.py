from odoo import models, fields, api

class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property',
        'salesperson',
        string='Properties',
        #domain=[('state', 'in', ['new', 'offer_received'])]
    )