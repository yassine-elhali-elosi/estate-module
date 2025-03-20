from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "An estate property type"
    _sql_constraints = [
        ('uniq_name', 'UNIQUE(name)', 'The property type name must be unique !')
    ]

    name = fields.Char('Property type', required=True)