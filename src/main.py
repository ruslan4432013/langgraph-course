# Импорты
from pprint import pprint

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages import trim_messages
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START, END

from src.settings import settings

# Инициализация модели
llm = ChatOpenAI(
    model="gpt-5.2",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
)

#
# # # Определение сообщений
# messages = [AIMessage("Итак, вы сказали, что исследуете океанские млекопитающие?", name="Bot")]
# messages.append(HumanMessage("Да, я знаю о китах. Но о чем я должен узнать?", name="Lance"))
#
# # Вывод сообщений
# for m in messages:
#     m.pretty_print()
#
# # Вызов модели
# print(llm.invoke(messages))

# Граф с MessagesState
# def chat_model_node(state: MessagesState):
#     return {"messages": [llm.invoke(state["messages"])]}
#
# builder = StateGraph(MessagesState)
# builder.add_node("chat_model", chat_model_node)
# builder.add_edge(START, "chat_model")
# builder.add_edge("chat_model", END)
# graph = builder.compile()
#
# # Вызов графа
# output = graph.invoke({'messages': messages})
# for m in output['messages']:
#     m.pretty_print()
#
# # Редьюсер с фильтрацией
# def filter_messages(state: MessagesState):
#     delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
#     return {"messages": delete_messages}
#
#
# def chat_model_node(state: MessagesState):
#     return {"messages": [llm.invoke(state["messages"])]}
#
#
# builder = StateGraph(MessagesState)
# builder.add_node("filter", filter_messages)
# builder.add_node("chat_model", chat_model_node)
# builder.add_edge(START, "filter")
# builder.add_edge("filter", "chat_model")
# builder.add_edge("chat_model", END)
# graph = builder.compile()
# #
# # # Тестовые сообщения
messages = [AIMessage("Hi.", name="Bot", id="1")]
messages.append(HumanMessage("Hi.", name="Lance", id="2"))
messages.append(AIMessage("So you said you were researching ocean mammals?", name="Bot", id="3"))
messages.append(HumanMessage("Yes, I know about whales. But what others should I learn about?", name="Lance", id="4"))


# #
# output = graph.invoke({'messages': messages})
# for m in output['messages']:
#     m.pretty_print()
#
# # Фильтрация при вызове модели
# print(llm.invoke(messages[-1:]))
#
#
# #
# # # Граф с фильтрацией
# def chat_model_node(state: MessagesState):
#     return {"messages": [llm.invoke(state["messages"][-1:])]}
#
#
# builder = StateGraph(MessagesState)
# builder.add_node("chat_model", chat_model_node)
# builder.add_edge(START, "chat_model")
# builder.add_edge("chat_model", END)
# graph = builder.compile()
#
# # Добавление новых сообщений
# messages.append(output['messages'][-1])
# messages.append(HumanMessage("Расскажи подробнее о нарвалах!", name="Lance"))
#
# # Вызов графа с фильтрацией
# output = graph.invoke({'messages': messages})
# for m in output['messages']:
#     m.pretty_print()


# # Обрезка сообщений
def chat_model_node(state: MessagesState):
    messages = trim_messages(
        state["messages"] + state["messages"] + state["messages"],
        max_tokens=50,
        strategy="last",
        token_counter=llm,
        allow_partial=False,
    )
    print('INITIAL MESSAGES')
    pprint(state["messages"])
    print('TRIMMED MESSAGES in node')
    pprint(messages)

    return {"messages": [llm.invoke(messages)]}


#
builder = StateGraph(MessagesState)
builder.add_node("chat_model", chat_model_node)
builder.add_edge(START, "chat_model")
builder.add_edge("chat_model", END)
graph = builder.compile()

# # Пример обрезки
messages.append(HumanMessage("Tell me where Orcas live!", name="Lance"))

# Вызов графа с обрезкой
messages_out_trim = graph.invoke({'messages': messages})
print(messages_out_trim)
