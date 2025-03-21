from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "An estate property type"
    _sql_constraints = [
        ('uniq_name', 'UNIQUE(name)', 'The property type name must be unique !')
    ]
    _order = "name"

    name = fields.Char('Property type', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')