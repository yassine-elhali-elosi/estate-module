from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sold_property(self):
        print(">>>>>>>>>>>>>>>test inherited estate_property.sold_property() method")
        self.env['account.move'].create(
            {
                'partner_id': self.buyer.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        "name": self.name,
                        "quantity": 1,
                        "price_unit": self.selling_price + 100.00 + (self.selling_price * 0.06)
                    })
                ]
            }
        )
        return super(EstateProperty, self).sold_property()