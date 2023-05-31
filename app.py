# Import libraries and modules
import os
import sys
import openai
from dotenv import load_dotenv
import json

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.memory import ConversationBufferMemory


# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

chatbot = ChatOpenAI(temperature=0, model="gpt-3.5-turbo",
                     openai_api_key=OPENAI_API_KEY)
memory = ConversationBufferMemory()


FormFields = [
    {
        "name": "FullName",
        "type": "text",
        "mandatory": True
    },
    {
        "name": "email",
        "type": "email",
        "mandatory": True
    },
    {
        "name": "phoneNumber",
        "type": "number",
        "mandatory": False
    },
    {
        "name": "birthdate",
        "type": "date",
        "mandatory": False
    }
]

# Define Form Fields
form_fields_str = "\n".join(
    [f"{field['name']}: {field['type']}, {'mandatory' if field['mandatory'] else 'optional'}" for field in FormFields])

# Define System Prompt Template
system_prompt_template = "Your job is to act as a form completion agent. You are required to collect the following pieces of information in a form.\n\n```\n{form_fields}\n```\n\nInstructions: - Ask for multiple pieces of information in one question but do not overwhelm the user. - Ask for the information in a very human way - Ensure that valid responses are provided - Correct the information as needed to account for user errors and fat fingering - Ensure that all mandatory pieces of information are provided - Nudge the user to provide optional pieces of information - After you have collected the information, summarize all the information for the user in a table and ask me to confirm. - Once confirmed, end by returning all information correctly formatted in a JSON format and code SYSTEM_EXIT in square brackets. Start with a greeting and the first question."

# Define System Prompt
system_message_prompt = SystemMessagePromptTemplate.from_template(
    system_prompt_template)

# Form System Message
system_message = system_message_prompt.format(
    form_fields=form_fields_str).content

# Add System Message to Memory
memory.chat_memory.messages.append(SystemMessage(content=system_message))


def get_response(user_input: str):
    if len(memory.chat_memory.messages) == 1:
        response = chatbot(memory.chat_memory.messages).content
        memory.chat_memory.add_ai_message(response)
        return response
    memory.chat_memory.add_user_message(user_input)
    response = chatbot(memory.chat_memory.messages).content
    memory.chat_memory.add_ai_message(response)
    return response


def main(user_input: str):
    user_input = sys.argv[1]
    response = get_response(user_input=user_input)
    print(response)

    while True:
        user_input = input('> ')

        # If the user types "exit", exit the loop
        if user_input.lower() == "exit":
            break

        response = get_response(user_input=user_input)
        print(response)


# Call the chat function to start the chat
if __name__ == "__main__":
    main(sys.argv[0])
