from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "An estate property tag"

    name = fields.Char('Tag name', required=True)