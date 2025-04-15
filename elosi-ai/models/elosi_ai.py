from odoo import models, fields, api
import os
import sys
from mistralai import Mistral
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm import main as llm

print(llm.TEMPLATE)

load_dotenv()

MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]

class ElosiAI(models.Model):
    _name = "elosi.ai"
    _description = "Elosi AI for ir.actions.server"

    input_prompt = fields.Text("Input Prompt")
    output_prompt = fields.Text("Output Prompt", store=True)
    output_result = fields.Text("Output Result", store=True)

    def generate_code(self):
        self.ensure_one() 
        print("Generating code for:", self.input_prompt)
        self.output_prompt = "Generating code..."
        client = Mistral(api_key=MISTRAL_API_KEY)

        mistral_response = client.agents.complete(
            agent_id = "ag:7e1f4155:20250414:untitled-agent:bb0a05f5",
            messages=[
                {
                    "role": "user",
                    "content": self.input_prompt
                }
            ]
        )

        print("Response from Mistral:", mistral_response)

        generated_code = mistral_response.choices[0].message.content

        #generated_code = "print(\"hello\")\n" + (self.input_prompt)
        self.output_prompt = generated_code

        print("Generated code:", generated_code)
        
        local_vars = {'self': self}
        exec(f"result = {generated_code}", local_vars)
        self.output_result = local_vars.get('result')
        print("Result:", self.output_result)

        self.input_prompt = ""
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'views': [[False, 'form']],
        }