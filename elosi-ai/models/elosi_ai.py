from odoo import models, fields, api
import os
import sys
from mistralai import Mistral
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm import main as llm

load_dotenv()

class ElosiAI(models.Model):
    _name = "elosi.ai"
    _description = "Elosi AI assistant"

    input_prompt = fields.Text("Input Prompt")
    output_prompt = fields.Text("Output Prompt", store=True)
    output_result = fields.Text("Output Result", store=True)
    state = fields.Selection([
        ('', 'Waiting'),
        ('generated', 'Generated')
    ], default='', string="State")

    def generate_code(self):
        self.ensure_one() 
        print("Generating code for:", self.input_prompt)
        self.output_prompt = "Generating code..."

        llm_response = llm.generate_code(self.input_prompt)

        print("Response from LLM:", llm_response)

        self.output_prompt = llm_response
        self.state = 'generated'
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'views': [[False, 'form']],
        }
        
    def reset_self(self):
        self.input_prompt = ""
        self.output_prompt = ""
        self.output_result = ""
        self.state = ""
    
    def send_feedback(self):
        feedback_value = self.env.context.get('feedback_value')
        print(feedback_value)
        # only for "yes" and "no" feedback for now, je dois traiter le cas où c'est "fix"
        llm.feedback(feedback_value, self.input_prompt, self.output_prompt)
        self.reset_self()