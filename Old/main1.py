# Import libraries and modules
import os
import openai
from langchain.llms import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_text(prompt):
    # Get the OpenAI API key from environment variables
    openai.api_key = openai_api_key

    # Call the OpenAI API with the prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": " + " + prompt},
        ]
    )

    # Return the response text
    return response["choices"][0]["message"]["content"]
    
# Define the prompt to send to the OpenAI API
prompt = "What is the meaning of life?"


# This is the main function which runs the flow of operations.
def main():
    response = generate_text(prompt)
    print(response)

# Run the main function with a form id
main()
