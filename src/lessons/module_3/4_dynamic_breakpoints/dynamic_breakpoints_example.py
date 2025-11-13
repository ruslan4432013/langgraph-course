from dynamic_breakpoints_graph import graph


initial_input = {"input": "hello world"}
thread_config = {"configurable": {"thread_id": "1"}}


print('\n[Запуск 1]')
# Запускаем граф до первого прерывания
for event in graph.stream(initial_input, thread_config, stream_mode="values"):
    print(event)


state = graph.get_state(thread_config)
print(state.next)

print(state.tasks)
#
print('\n [Запуск 2]')
for event in graph.stream(None, thread_config, stream_mode="values"):
    print(event)
#
state = graph.get_state(thread_config)
print(state.next)

print('\n Обновляем состояние...')
graph.update_state(
    thread_config,
    {"input": "hi"},
)

print('\n [Запуск 3]')
for event in graph.stream(None, thread_config, stream_mode="values"):
    print(event)