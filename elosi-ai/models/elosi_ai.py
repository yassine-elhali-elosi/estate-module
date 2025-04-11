from odoo import models, fields, api
import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]

class ElosiAI(models.Model):
    _name = "elosi.ai"
    _description = "Elosi AI for ir.actions.server"

    input_prompt = fields.Text("Input Prompt")
    output_prompt = fields.Text("Output Prompt", store=True)

    def generate_code(self):
        for record in self:
            print("Generating code for:", record.input_prompt)
            client = Mistral(api_key=MISTRAL_API_KEY)

            mistral_response = client.agents.complete(
                agent_id = "ag:7e1f4155:20250410:untitled-agent:a8450e92",
                messages=[
                    {
                        "role": "user",
                        "content": record.input_prompt
                    }
                ]
            )

            generated_code = mistral_response.choices[0].message.content
            record.output_prompt = generated_code
        
        return True