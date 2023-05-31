import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("Your job is to act as a form completion agent. You are required to collect the full name, phone number, and email address of the user. All three fields are required. Do not give up until you collect all information. Feel free to ask for multiple pieces of information in one pass. Make sure all pieces of information provided are valid. Phone number must have ISD code in it. Sufficient to ask the user which country the phone number is from and then you add ISD code to it. Once you have collected all the information, present all information to the user and ask them to confirm. Once you have finished, say thank you and exit. "),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

llm = OpenAI(
    temperature=0.1,
    openai_api_key=OPENAI_API_KEY,
    model_name='gpt-3.5-turbo'  # can be used with llms like 'gpt-3.5-turbo'
)

memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)


# print(conversation.predict(input="Good morning!"))
# -> 'Hello! How can I assist you today?'

def chat():
    print(conversation.predict(input=""))
    while True:
        user_input = input('> ')

        # If the user types "exit", exit the loop
        if user_input.lower() == "exit":
            break

        response = conversation.predict(input=user_input)
        print(response)


# Call the chat function to start the chat
chat()
