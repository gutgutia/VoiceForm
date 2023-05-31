# Import libraries and modules
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory,
                                                  ConversationSummaryMemory,
                                                  ConversationBufferWindowMemory,
                                                  ConversationKGMemory)
from langchain.callbacks import get_openai_callback
import tiktoken

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = OpenAI(
    temperature=0,
    openai_api_key=OPENAI_API_KEY,
    model_name='text-davinci-003'  # can be used with llms like 'gpt-3.5-turbo'
)


def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        print(f'Spent a total of {cb.total_tokens} tokens')
    return result


conversation_buf = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory()
)


def chat():
    while True:
        user_input = input('> ')

        # If the user types "exit", exit the loop
        if user_input.lower() == "exit":
            break

        response = conversation_buf(user_input)['response']
        print(response)


# Call the chat function to start the chat
chat()
