from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="codestral")

template = """
You are an expert Odoo backend developer.
Only return the Python code — no explanations, no comments.
The code must be valid, safe, and ready to run inside an Odoo server action.
You understand models like res.partner, sale.order, crm, and typical business flows.
Always assume the env variable is available.
Use clear logic and avoid hardcoded IDs.
Import libraries where necessary.

Here is the prompt:
{input_prompt}
"""

prompt = ChatPromptTemplate(template)
chain = prompt | model

chain.invoke(
    {
        "input_prompt": "Create a method that returns the name of the partner with ID 1",
    }
)