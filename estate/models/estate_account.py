from odoo import models, fields, api

class EstateAccount(models.Model):
    _name = "estate.account"
    _description = "Link between estate and account modules"
    