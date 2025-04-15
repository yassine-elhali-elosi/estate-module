from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="codellama:7b")

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

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

try:
    result = chain.invoke(
        {
            "input_prompt": "Return the name of the partner with ID 1",
        }
    )
    print(result)
except Exception as e:
    print(f"An error occurred: {e}")