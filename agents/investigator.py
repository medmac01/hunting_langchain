from langchain_community.llms import Ollama

from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from tools.cve_avd_tool import CVESearchTool
from tools.misp_tool import MispTool

from langchain.agents import initialize_agent, AgentType, load_tools

from dotenv import load_dotenv
import os

load_dotenv()

llm = Ollama(model="openhermes", base_url=os.getenv('OLLAMA_HOST'), temperature=0.1, num_predict=-1)
wrn = Ollama(model="wrn", base_url=os.getenv('OLLAMA_HOST'))
llama3 = Ollama(model="llama3", base_url=os.getenv('OLLAMA_HOST'))


cve_search_tool = CVESearchTool().cvesearch
misp_search_tool =  MispTool().search
misp_search_by_date_tool = MispTool().search_by_date

tools = [cve_search_tool, misp_search_tool, misp_search_by_date_tool]

# conversational agent memory
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=3,
    return_messages=True
)


# create our agent
conversational_agent = initialize_agent(
    # agent="chat-conversational-react-description",
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    memory=memory,
    early_stopping_method='generate',
    handle_parsing_errors=True
)

def invoke(input_text):
    return conversational_agent({"input":input_text})