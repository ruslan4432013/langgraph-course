from src.editting_state_intro.agent_with_human_feedback import graph

# Входные данные
initial_input = {"messages": "Умножьте 2 и 3"}

# Поток
thread = {"configurable": {"thread_id": "5"}}

# Запуск графа до первого прерывания
for event in graph.stream(initial_input, thread, stream_mode="values"):
    print(event["messages"][-1])

# Получение ввода пользователя
user_input = input("Скажите, как вы хотите обновить состояние: ")

# Теперь обновляем состояние, как если бы мы были узлом human_feedback
graph.update_state(thread, {"messages": user_input}, as_node="human_feedback")

state = graph.get_state(thread).values

print('update state [START]')
for m in state["messages"]:
    print(m)
print('update state [END]')

# Продолжение выполнения графа
for event in graph.stream(None, thread, stream_mode="values"):
    print(event["messages"][-1])

# Продолжение выполнения графа
for event in graph.stream(None, thread, stream_mode="values"):
    print(event["messages"][-1])
