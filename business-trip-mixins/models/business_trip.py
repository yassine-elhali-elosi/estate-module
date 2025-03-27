from odoo import models, fields

class BusinessTrip(models.Model):
    _name = "business.trip"
    _inherit = ["mail.thread"]
    _description = "Business Trip"

    name = fields.Char()
    partner_id = fields.Many2one("res.partner", "Responsible")
    guest_ids = fields.Many2many("res.partner", "Participants")