from odoo import models, fields

class BusinessTrip(models.Model):
    _name = "business.trip"
    _inherit = ["mail.thread"]
    _description = "Business Trip"

    name = fields.Char(tracking=True)
    partner_id = fields.Many2one("res.partner", "Responsible", tracking=True)
    guest_ids = fields.Many2many("res.partner", "Participants")