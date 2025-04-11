from odoo import models, fields, api

class ElosiAI(models.Model):
    _name = "elosi.ai"
    _description = "Elosi AI for ir.actions.server"

    input_prompt = fields.Text("Input Prompt", required=True)
    output_prompt = fields.Text("Output Prompt", compute="_compute_output_prompt", store=True)

    @api.depends("input_prompt")
    def _compute_output_prompt(self):
        for record in self:
            print("input :", record.input_prompt)
            print("Generating output prompt...")
            record.output_prompt = "print(\"hello\")"
            print("Output prompt generated:", record.output_prompt)