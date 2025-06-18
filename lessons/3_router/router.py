import json
from pyexpat.errors import messages

from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers a and b"""
    return a * b

llm = ChatDeepSeek(
    model='deepseek-chat',
    temperature=0.1,
    max_retries=2,
    api_base="https://api.proxyapi.ru/deepseek"  # Необходимо, для работы модели через ProxyApi
)

llm_with_tools = llm.bind_tools([multiply])


class BasicToolNode:
    def __init__(self, tools: list):
        self.tool_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):

        if messages := inputs.get("messages", []):
            last_message = messages[-1]
        else:
            raise ValueError('Нет сообщений в входных данных')

        outputs = []

        for tool_call in last_message.tool_calls:
            tool_result = self.tool_by_name[tool_call['name']].invoke(tool_call['args'])
            outputs.append(ToolMessage(content=json.dumps(tool_result), name=tool_call['name'], tool_call_id=tool_call['id']))

        return {'messages': outputs}

def tools_condition(state):
    last_message = state.get('messages', [])[-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(last_message)
        return 'tools'

    return END

class State(MessagesState):
    ...

def tool_calling_llm(state):
    return {'messages': llm_with_tools.invoke(state['messages'])}

builder = StateGraph(State)

builder.add_node('tools', BasicToolNode(tools=[multiply]))
builder.add_node('tool_calling_llm', tool_calling_llm)

builder.add_edge(START, 'tool_calling_llm')
builder.add_conditional_edges('tool_calling_llm', tools_condition)
builder.add_edge('tools', END)

graph = builder.compile()

from langchain_core.messages import HumanMessage

result = graph.invoke({"messages": [HumanMessage(content="Привет! Как дела?")]})
for msg in result["messages"]:
    print(f"[{msg.type}]: {msg.content}")
