from langchain_core.messages import HumanMessage

from src.breakpoints_intro.react import graph

# Входные данные
initial_input = {"messages": HumanMessage(content="Умножь 2 на 3")}

# # Поток
# thread = {"configurable": {"thread_id": "1"}}
#
# # Запуск графа до первого прерывания
# for event in graph.stream(initial_input, thread, stream_mode="values"):
#     last_message = event['messages'][-1]
#     print(f'[{type(last_message).__name__}]: ', last_message)
#
# # Мы можем получить состояние и посмотреть на следующий узел для вызова.
# # Это удобный способ увидеть, что граф был прерван.
# state = graph.get_state(thread)
# print(f'{state.next=}')
#
# # Теперь введем удобный трюк. Когда мы вызываем граф с `None`, он просто продолжит выполнение с последней контрольной точки состояния!
# # Для ясности, LangGraph повторно выдаст текущее состояние, которое содержит `AIMessage` с вызовом инструмента.
# # Затем он продолжит выполнение следующих шагов в графе, начиная с узла инструмента.
# # Мы видим, что узел инструмента выполняется с этим вызовом инструмента, и он передается обратно в чат-модель для нашего окончательного ответа.
# for event in graph.stream(None, thread, stream_mode="values"):
#     last_message = event['messages'][-1]
#     print(f'[{type(last_message).__name__}]: ', last_message)

# Теперь объединим это с конкретным шагом подтверждения пользователем, который принимает ввод пользователя.
# Входные данные
initial_input = {"messages": HumanMessage(content="Умножь 2 на 3")}

# Поток
thread = {"configurable": {"thread_id": "2"}}

# Запуск графа до первого прерывания
for event in graph.stream(initial_input, thread, stream_mode="values"):
    last_message = event['messages'][-1]
    print(f'[{type(last_message).__name__}]: ', last_message)

# Получение подтверждения пользователя
user_approval = input("Вы хотите вызвать инструмент? (да/нет): ")

# Проверка подтверждения
if user_approval.lower() == "да":
    # Если подтверждено, продолжить выполнение графа
    for event in graph.stream(None, thread, stream_mode="values"):
        last_message = event['messages'][-1]
        print(f'[{type(last_message).__name__}]: ', last_message)
else:
    print("Операция отменена пользователем.")
