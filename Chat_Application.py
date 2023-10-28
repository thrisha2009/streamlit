from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ConversationChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import json
from ccd_text_split import *

llm = OpenAI(temperature=1, openai_api_key='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')
llm_chat = ChatOpenAI(temperature=1, openai_api_key="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")


tools = load_tools(["wikipedia", "llm-math"], llm=llm)

def langchain_interaction(user_input):
    
    agent = initialize_agent(tools, llm, agent= AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    
    langchain_response = agent.run(user_input)
    
    return langchain_response


def chat_reply(template, user_input):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(template), HumanMessagePromptTemplate.from_template("{input}")
    ])
    conversation = ConversationChain(prompt=prompt, llm=llm_chat)
    return conversation.predict(input=user_input)

def instruction_llm(template, query):
    chain = LLMChain(llm=llm, prompt=PromptTemplate(template=template, input_variables=['query']))
    return chain.run(query=query)


def check_language(user_input):
    template = "Check whether the {query} is in English or another language. If it is in English, reply 'Yes' else reply 'No'"
    return instruction_llm(template, query=user_input)


def process_input_type(query):
    template_file_path = "/root/Programs/Tree_OpenAi_v2/content/identify_sentence.txt"
    with open(template_file_path, 'r') as file:
        template_sentence = file.read()
    ans = instruction_llm(template_sentence, query=query)
    return ans


def response_generator(filepath,user_input,template_file_path):
    question_response_dict = {}
    with open(filepath, 'r') as file:
        template_sentence = json.load(file)        
    for entry in template_sentence:
        question = entry.get('question')
        response = entry.get('response')
        question_response_dict[question]= response    

    if user_input in question_response_dict:
        return question_response_dict[user_input]
    else:  
        #template_file_path = "/root/Programs/Tree_OpenAi_v2/content/template.txt"
        with open(template_file_path, 'r') as file:
            template = file.read()
        return chat_reply( template,user_input)
    
def main_process(user_input):
    
    if 'Yes' in check_language(user_input):
        
        result = process_input_type(user_input)
        if 'Greeting' in result:
            return response_generator('/root/Programs/Tree_OpenAi_v2/json files/1_greetings.json', user_input, '/root/Programs/Tree_OpenAi_v2/content/Greeting_prompt.txt')
        
        elif 'Compliment' in result:
            return response_generator('/root/Programs/Tree_OpenAi_v2/json files/2_compliments.json',user_input, '/root/Programs/Tree_OpenAi_v2/content/Compliments_prompt.txt')
        
        elif 'Personal' in result:
            return response_generator('/root/Programs/Tree_OpenAi_v2/json files/3_personal.json',user_input, '/root/Programs/Tree_OpenAi_v2/content/Personal_prompt.txt')
            
        elif 'Offensive' in result:
            return response_generator('/root/Programs/Tree_OpenAi_v2/json files/4_offensive.json',user_input,'/root/Programs/Tree_OpenAi_v2/content/Offensive_prompt.txt')
        
        elif 'Database' in result:
            #print('\n AI:  ',response_generator('/root/Programs/Tree_OpenAi_v2/json files/5_database.json',user_input))
            context = product_qa(user_input)
            with open('/root/Programs/Tree_OpenAi_v2/content/Database_prompt.txt', 'r') as file:
                template = file.read()
            template = template + context + "{history}"
            return chat_reply(template,user_input)
        else:
            langchain_response = langchain_interaction(user_input)
            return langchain_response

    else:
        return 'type in english'
    
def post_processor(text):
    template = """You are an Intelligent chatbot. You have to check the input given by the AI for offensive, harsh or informal content .
                You have to change the input into polite, non - offensive and formal , without harsh words, also be precise without changing the context of input 
                {history}"""
    return chat_reply(template,text)
    
def chatbot(user_input):
    res = main_process(user_input)
    return post_processor(res)

'''
while True:
    user_input = input("\n Human:   ")
    
    if user_input.lower() in ('exit', 'quit', 'bye'):    
        break
    print('\n AI:',chatbot(user_input))
'''
