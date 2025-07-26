import pprint

from langchain_core.messages import HumanMessage
from agent import graph
# Запустим его, как и раньше
# Входные данные

initial_input = {"messages": HumanMessage(content="Умножь 2 и 3")}

# Поток
thread = {"configurable": {"thread_id": "1"}}

# Запускаем граф до первой остановки
for event in graph.stream(initial_input, thread, stream_mode="values"):
    print(event['messages'][-1])

print('[Состояние]:')
print(graph.get_state(thread))

print('[История графа]:')
all_states = [s for s in graph.get_state_history(thread)]
pprint.pprint(all_states)
print(len(all_states))

print('[Предпоследнее состояние]')
to_replay = all_states[-2]
print(to_replay)

print('[to_replay.values]')
print(to_replay.values)

print('[to_replay.next]')
print(to_replay.next)

print('[to_replay.config]')
print(to_replay.config)

print('[Откатываем граф]')
for event in graph.stream(None, to_replay.config, stream_mode="values"):
    print(event['messages'][-1])


print('[Сообщения в ветвлении]')
to_fork = all_states[-2]
print(to_fork.values["messages"])

print('[Конфигурация ветвления]')
print(to_fork.config)

print('[Обновляем конфигурацию ветвления]')
fork_config = graph.update_state(
  to_fork.config,
  {"messages": [HumanMessage(content='Умножь 5 на 3', id=to_fork.values["messages"][0].id)]},
)
print(fork_config)

print('[Перезапрашиваем историю]')
all_states = [state for state in graph.get_state_history(thread) ]
print('[Получаем наши сообщения в том же графе]')
print(all_states[0].values["messages"])
print('[Получаем новое состояние]')
print(graph.get_state({'configurable': {'thread_id': '1'}}))

print('[Запускаем граф с новой веткой]')
for event in graph.stream(None, fork_config, stream_mode="values"):
  print(event['messages'][-1])

print('[Обновленное состояние нашего графа после выполнения]')
print(graph.get_state({'configurable': {'thread_id': '1'}}))
pprint.pprint(graph.get_state({'configurable': {'thread_id': '1'}}).values['messages'])