from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from typing import TypedDict,Annotated
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
load_dotenv()
import requests


class chat_state(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

search_tool=DuckDuckGoSearchRun()
@tool
def calculator(first_num:float,second_num:float,operation:str)->float:
    """perform the basic arthmetic operations on two numbers
       supported operation:add,sum,mul,division
    """
    if operation=="add":
        result=first_num+second_num
    elif operation=="sub":
        result=first_num-second_num
    elif operation=="mul":
        result=first_num*second_num
    elif operation=="division":
        if second_num==0:
            return {"error":"division by zero not allowed"}
        result=first_num/second_num
    else:
        return {"error":"unsupported operation"}
    return result

@tool
def get_stock_price(symbol:str)->dict:
   """
    fetch the laetest stock price of symbol (e.g. 'AAPL','TSLA')
    using Alpha Vantage with API Key in the url
   """
   url=f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&interval=5min&apikey=FTRUHCYT0E41Q2XA2"
   r=requests.get(url)
   return r.json()

llm=ChatGroq(
    model="openai/gpt-oss-20b"
)

tools=[search_tool,calculator,get_stock_price]

llm_with_tool=llm.bind_tools(tools)

def chat_node(state:chat_state):
    messages=state['messages']
    response=llm_with_tool.invoke(messages)
    return {'messages':[response]}


tool_node=ToolNode(tools)

graph=StateGraph(chat_state)
graph.add_node("chat_node",chat_node)
graph.add_node("tool_node",tool_node)

graph.add_edge(START,"chat_node")
graph.add_conditional_edges("chat_node",tools_condition ,{
        "tools": "tool_node",
        "__end__": END
    })
graph.add_edge("tool_node","chat_node")

chatbot=graph.compile()
res=chatbot.invoke({'messages':[HumanMessage(content="get the stock of AAPL by using the tool")]})
print(res['messages'][-1].content)

