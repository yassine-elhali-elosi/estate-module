from odoo import models, api

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sold_property(self):
        print(">>>>>>>>>>>>>>>test inherited estate_property.sold_property() method")
        return super(EstateProperty, self).sold_property()