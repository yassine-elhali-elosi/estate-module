from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "An estate property tag"
    _sql_constraints = [
        ('uniq_name', 'UNIQUE(name)', 'The tag name must be unique')
    ]
    _order = "name"

    name = fields.Char('Tag name', required=True)
    color = fields.Integer('Color')