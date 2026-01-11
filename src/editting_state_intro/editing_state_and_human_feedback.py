from langchain_core.messages import HumanMessage

from src.editting_state_intro.agent_with_human_feedback import graph

# Входные данные
initial_input = {"messages": "Умножь 2 и 3"}

# Поток
thread = {"configurable": {"thread_id": "1"}}

# Запуск графа до первого прерывания
print('Interrupt[START]')
for event in graph.stream(initial_input, thread, stream_mode="values"):
    print(event['messages'][-1])

state = graph.get_state(thread)
print(state)

print('Interrupt[END]')
# Теперь мы можем напрямую применить обновление состояния. Помните, что обновления ключа `messages` будут использовать редьюсер `add_messages`:
# * Если мы хотим перезаписать существующее сообщение, мы можем указать `id` сообщения.
# * Если мы просто хотим добавить к нашему списку сообщений, то мы можем передать сообщение без указания `id`, как показано ниже.
graph.update_state(
    thread,
    {"messages": [HumanMessage(content="Нет, на самом деле умножь 3 и 3!")]},
)
#
# Посмотрим
# Мы вызвали `update_state` с новым сообщением. Редьюсер `add_messages` добавляет его к нашему ключу состояния `messages`.
new_state = graph.get_state(thread).values
print('new_state[START]')
for m in new_state['messages']:
    print(m)
print('new_state[END]')
#
# state = graph.get_state(thread)
# print(state.next)
#
# Теперь продолжим работу с нашим агентом, просто передав `None` и позволив ему продолжить с текущего состояния.
# Мы выдаем текущее состояние, а затем переходим к выполнению оставшихся узлов.
for event in graph.stream(None, thread, stream_mode="values"):
    print(event['messages'][-1])

# Теперь мы вернулись к `assistant`, у которого есть наша `точка остановки`. Мы снова можем передать `None` для продолжения.
for event in graph.stream(None, thread, stream_mode="values"):
    print(event['messages'][-1])
