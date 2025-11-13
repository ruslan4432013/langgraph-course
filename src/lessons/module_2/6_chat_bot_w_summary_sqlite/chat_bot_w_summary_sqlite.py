import pprint
import sqlite3

from langchain_openai import ChatOpenAI

from src.settings import settings

# В памяти
conn = sqlite3.connect(":memory:", check_same_thread=False)

db_path = "state_db/example.db"
conn = sqlite3.connect(db_path, check_same_thread=False)

# Вот наш чекпоинтер
from langgraph.checkpoint.sqlite import SqliteSaver

memory = SqliteSaver(conn)

from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langgraph.graph import END
from langgraph.graph import MessagesState

model = ChatOpenAI(
    api_key=settings.API_KEY,
    model='gpt-4o-mini',
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1",  # Необходимо, для работы модели через ProxyApi
)


class State(MessagesState):
    summary: str


# Определяем логику вызова модели
def call_model(state: State):
    # Получаем сводку, если она есть
    summary = state.get("summary", "")

    # Если сводка есть, добавляем её
    if summary:
        # Добавляем сводку в системное сообщение
        system_message = f"Сводка предыдущего разговора: {summary}"
        # Добавляем сводку к новым сообщениям
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = state["messages"]
    pprint.pprint(messages)
    print(len(messages))
    response = model.invoke(messages)
    return {"messages": response}


def summarize_conversation(state: State):
    # Сначала получаем существующую сводку
    summary = state.get("summary", "")

    # Создаём промпт для сводки
    if summary:
        # Сводка уже существует
        summary_message = (
            f"Это сводка разговора на данный момент: {summary}\n\n"
            "Дополните сводку, учитывая новые сообщения выше:"
        )
    else:
        summary_message = "Создайте сводку разговора выше:"

    # Добавляем промпт в историю
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    # Удаляем все сообщения, кроме двух последних
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}


# Определяем, завершить или суммировать разговор
def should_continue(state: State):
    """Возвращает следующий узел для выполнения."""
    messages = state["messages"]

    # Если сообщений больше шести, суммируем разговор
    if len(messages) > 6:
        return "summarize_conversation"

    # Иначе завершаем
    return END


from langgraph.graph import StateGraph, START

# Определяем новый граф
workflow = StateGraph(State)
workflow.add_node("conversation", call_model)
workflow.add_node(summarize_conversation)

# Устанавливаем точку входа как "conversation"
workflow.add_edge(START, "conversation")
workflow.add_conditional_edges("conversation", should_continue)
workflow.add_edge("summarize_conversation", END)

# Компилируем
graph = workflow.compile(checkpointer=memory)

# Создаём тред
config = {"configurable": {"thread_id": "1"}}

# Начинаем разговор
input_message = HumanMessage(content="Привет! Я Лэнс")
print(graph.invoke({"messages": [input_message]}, config))

input_message = HumanMessage(content="Как меня зовут?")
print(graph.invoke({"messages": [input_message]}, config))

input_message = HumanMessage(content="Мне нравятся 49ers!")
print(graph.invoke({"messages": [input_message]}, config))

# # Создать конфигурацию потока
# config = {"configurable": {"thread_id": "1"}}
# graph_state = graph.get_state(config)
# print(graph_state)
