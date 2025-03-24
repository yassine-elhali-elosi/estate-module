from odoo import models, api

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sold_property(self):
        print(">>>>>>>>>>>>>>>test inherited estate_property.sold_property() method")
        self.env['account.move'].create(
            {
                'partner_id': self.buyer.id,
                'move_type': 'out_invoice'
            }
        )
        return super(EstateProperty, self).sold_property()