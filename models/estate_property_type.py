from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "An estate property type"

    name = fields.Char('Property type', required=True)