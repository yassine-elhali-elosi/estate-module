import re
from odoo import models, fields

class BusinessExpense(models.Model):
    _name = "business.expense"
    _inherit = ["mail.thread"]
    _description = "Business Expense"

    name = fields.Char()
    amount = fields.Float("Amount")
    trip_id = fields.Many2one("business.trip", "Business Trip")
    partner_id = fields.Many2one("res.partner", "Created by")

    def message_new(self, msg, custom_values=None):
        name = msg.get("subject", "New Expense")
        email_from = msg.get("email_from")

        amount_pattern = '(\d+(\.\d*)?|\.\d+)'
        expense_price = re.findall(amount_pattern, name)
        price = expense_price and float(expense_price[-1][0]) or 1.0

        partner = self.env["res.partner"].search(["email", "like", email_from], limit=1)

        defaults = {
            "name": name,
            "amount": price,
            "partner_id": partner.id
        }
        defaults.update(custom_values or {})
        res = super().message_new(msg, custom_values=defaults)
        return res