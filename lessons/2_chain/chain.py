from pprint import pprint
from typing import Annotated

from langchain_core.messages import AIMessage, HumanMessage
import os
from langchain_deepseek import ChatDeepSeek
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph import MessagesState

messages = [
    AIMessage(content="Вы говорили, что исследуете морских млекопитающих?", name="Модель"),
    HumanMessage(content="Да, верно.", name="Лэнс"),
    AIMessage(content="Отлично, о чём бы вы хотели узнать?", name="Модель"),
    HumanMessage(content="Хочу узнать лучшее место для наблюдения за косатками в США.", name="Лэнс")
]

# Установка API-ключа
if "DEEPSEEK_API_KEY" not in os.environ:
    os.environ["DEEPSEEK_API_KEY"] = input("DEEPSEEK_API_KEY: ")
#
llm = ChatDeepSeek(
    model='deepseek-chat',
    temperature=0.1,
    max_retries=2,
    api_base="https://api.proxyapi.ru/deepseek"  # Необходимо, для работы модели через ProxyApi
)

############### Проверка 1. ###############
# response = llm.invoke(messages)
# print(response.content)
###########################################


def multiply(a: int, b: int) -> int:
    """Перемножает два числа."""
    return a * b

llm_with_tools = llm.bind_tools([multiply])

############### Проверка 2. ###############
# response = llm.invoke(messages)
# print(response.content)

# response = llm_with_tools.invoke([HumanMessage(content="Умножь 2 на 3")])
# print(response.tool_calls) # [{'name': 'multiply', 'args': {'a': 2, 'b': 3}, 'id': 'call_P8VTlydPKGGrR1tq6DExAI5L', 'type': 'tool_call'}]
###########################################


# class MessagesState(TypedDict):
#     messages: list[AnyMessage]

# class MessagesState(TypedDict):
#     messages: Annotated[list[AnyMessage], add_messages]

class CustomState(MessagesState):
    # Здесь можно добавить дополнительные ключи для состояния графа
    pass

############### Проверка 3. ###############
# # Изначальное состояние
# initial_messages = [AIMessage(content="Hello! How can I assist you?", name="Модель"),
#                     HumanMessage(content="Я ищу информацию по морской биологии.", name="Lance")
#                    ]
#
# # Новые сообщения для добавления
# new_message = AIMessage(content="Конечно, я могу помочь с этим. Что конкретно вас интересует?", name="Модель")
#
# # Тест
# pprint(add_messages(initial_messages , new_message))
###########################################

# Узел: вызов модели с инструментами
def tool_node(state: CustomState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# Сборка графа
builder = StateGraph(CustomState)
builder.add_node("tool_node", tool_node)
builder.add_edge(START, "tool_node")
builder.add_edge("tool_node", END)
graph = builder.compile()

if __name__ == '__main__':
    """
    Демонстрация работы графа.
    """
    # Без вызова инструмента
    result = graph.invoke({"messages": [HumanMessage(content="Привет!")]})
    for msg in result["messages"]:
        print(f"{msg.name}: {msg.content}")

    # С вызовом инструмента
    result = graph.invoke({"messages": [HumanMessage(content="Умножь 5 на 8")]})
    for msg in result["messages"]:
        if hasattr(msg, 'tool_calls'):
            print(f"Вызов инструмента: {msg.tool_calls[0]['name']} с аргументами {msg.tool_calls[0]['args']}")

    pprint(result['messages'])

