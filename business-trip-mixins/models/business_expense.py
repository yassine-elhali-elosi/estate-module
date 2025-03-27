from odoo import models, fields

class BusinessExpense(models.Model):
    _name = "business.expense"
    _inherit = ["mail.thread"]
    _description = "Business Expense"

    name = fields.Char()
    amount = fields.Float("Amount")
    trip_id = fields.Many2one("business.trip", "Business Trip")
    partner_id = fields.Many2one("res.partner", "Created by")