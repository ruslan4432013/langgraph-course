# Установка и инициализация модели LLM (в данном случае ChatDeepSeek)
from typing import Literal

from langchain_openai import ChatOpenAI

from src.settings import settings

model = ChatOpenAI(
    model="gpt-5.2",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
)

# # Использование MessagesState и расширение его пользовательским полем `summary`
from langgraph.graph import MessagesState


class State(MessagesState):
    summary: str


#
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage


#
#
# # Определяем логику вызова модели
def call_model(state: State):
    # Получаем резюме, если оно существует
    summary = state.get("summary", "")

    # Если есть резюме, добавляем его
    if summary:
        # Добавляем резюме в системное сообщение
        system_message = f"Резюме предыдущей беседы: {summary}"
        # Добавляем резюме к новым сообщениям
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = state["messages"]

    response = model.invoke(messages)
    return {"messages": response}


#
def summarize_conversation(state: State):
    # Сначала получаем существующее резюме
    summary = state.get("summary", "")

    # Создаём подсказку для суммирования
    if summary:
        # Резюме уже существует
        summary_message = (
            f"Это резюме беседы на данный момент: {summary}\n\n"
            "Расширь резюме, учитывая новые сообщения выше:"
        )
    else:
        summary_message = "Создайте резюме беседы выше:"

    # Добавляем подсказку в историю
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    # Удаляем все сообщения, кроме двух последних
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}


#
#
from langgraph.graph import END


#
#
# # Определяем, нужно ли завершать или суммировать беседу
def should_continue(state: State) -> Literal['summarize_conversation', END]:
    """Возвращает следующий узел для выполнения."""
    messages = state["messages"]

    # Если сообщений больше шести, суммируем беседу
    if len(messages) > 6:
        return "summarize_conversation"
    # Иначе можно завершить
    return END


#
#
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START

# Определяем новый граф
workflow = StateGraph(State)
workflow.add_node("conversation", call_model)
workflow.add_node("summarize_conversation", summarize_conversation)

# Устанавливаем точку входа как "conversation"
workflow.add_edge(START, "conversation")
workflow.add_conditional_edges("conversation", should_continue)
workflow.add_edge("summarize_conversation", END)

# Компилируем с памятью
memory = MemorySaver()
graph = workflow.compile()
# #
# #
# # # Создать поток
# config = {"configurable": {"thread_id": "1"}}
# #
# # # Начать беседу
# input_message = HumanMessage(content="Привет! Я Ланс")
# output = graph.invoke({"messages": [input_message]}, config)
# for m in output['messages'][-1:]:
#     m.pretty_print()
# #
# input_message = HumanMessage(content="Как меня зовут?")
# output = graph.invoke({"messages": [input_message]}, config)
# for m in output['messages'][-1:]:
#     m.pretty_print()
# #
# input_message = HumanMessage(content="Мне нравятся 49 летние!")
# output = graph.invoke({"messages": [input_message]}, config)
# for m in output['messages'][-1:]:
#     m.pretty_print()
# #
# #
# input_message = HumanMessage(content="Мне нравится Ник Боса, разве он не самый высокооплачиваемый защитник?")
# output = graph.invoke({"messages": [input_message]}, config)
# for m in output['messages'][-1:]:
#     m.pretty_print()
#
# print('SUMMARY:')
# print(graph.get_state(config).values.get("summary",""))
#
