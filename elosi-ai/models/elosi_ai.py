from odoo import models, fields, api

class ElosiAI(models.Model):
    _name = "elosi.ai"
    _description = "Elosi AI for ir.actions.server"

    input_prompt = fields.Text("Input Prompt", required=True)
    output_prompt = fields.Text("Output Prompt", compute="_compute_output_prompt")

    @api.depends("input_prompt")
    def _compute_output_prompt(self):
        print(self.input_prompt)

        if self.input_prompt:
            print("Generating output prompt...")
            print("Output prompt generated.")