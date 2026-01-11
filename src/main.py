import json
from typing import Literal

from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph

from src.settings import settings


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers a and b"""
    return a * b


llm = ChatOpenAI(
    model="gpt-5.2",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
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
            outputs.append(
                ToolMessage(content=json.dumps(tool_result), name=tool_call['name'], tool_call_id=tool_call['id']))

        return {'messages': outputs}


class State(MessagesState):
    ...


def tool_calling_llm(state):
    return {'messages': llm_with_tools.invoke(state['messages'])}


def tools_condition(state: State) -> Literal['tools', END]:
    last_message = state.get('messages', [])[-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return 'tools'

    return END


builder = StateGraph(State)

builder.add_node('tools', BasicToolNode(tools=[multiply]))
builder.add_node('tool_calling_llm', tool_calling_llm)

builder.add_edge(START, 'tool_calling_llm')
builder.add_conditional_edges('tool_calling_llm', tools_condition)
builder.add_edge('tools', END)

graph = builder.compile()

if __name__ == '__main__':
    from langchain_core.messages import HumanMessage

    result = graph.invoke({"messages": [HumanMessage(content="Сколько будет 2 * 3?")]})
    for msg in result["messages"]:
        msg.pretty_print()
