Этот набор файлов демонстрирует все ключевые концепции из методички
с практическими примерами для каждого раздела.

СОДЕРЖАНИЕ ФАЙЛОВ
=================

01_invoke.py
------------
Метод invoke - синхронный вызов одного входа
Включает:
- Базовое использование invoke
- Использование конфигурации (run_name, tags, metadata)
- Примеры с простыми и сложными функциями

Запуск: python 01_invoke.py


02_batch.py
-----------
Метод batch - пакетная обработка нескольких входов
Включает:
- Параллельная обработка списков входов
- Контроль параллелизма через max_concurrency
- Обработка ошибок с return_exceptions

Запуск: python 02_batch.py


03_stream.py
------------
Методы stream и astream - потоковая передача данных
Включает:
- Базовая потоковая передача
- RunnableGenerator для истинной потоковой передачи
- Асинхронные операции (astream)
- Интеграция потоковой передачи в конвейеры

Запуск: python 03_stream.py


04_runnable_config.py
---------------------
RunnableConfig - конфигурация выполнения
Включает:
- Основные параметры конфигурации (run_name, run_id, tags, metadata)
- Использование max_concurrency для контроля параллелизма
- Настраиваемые параметры через configurable
- Передача одной конфигурации для batch

Запуск: python 04_runnable_config.py


05_composition.py
-----------------
Композиция Runnable - построение цепочек
Включает:
- RunnableSequence (последовательная композиция с |)
- RunnableParallel (параллельная композиция со словарями)
- Метод pipe() для явной композиции
- Смешанные композиции (последовательность + параллель)
- Batch для составных цепочек

Запуск: python 05_composition.py


06_custom_runnable.py
---------------------
Пользовательские Runnable (RunnableLambda, RunnableGenerator)
Включает:
- RunnableLambda для обертывания функций
- RunnableGenerator для генераторов и потоковой передачи
- Преобразование типов в runnable
- Композиция пользовательских runnable
- Использование конфигурации с пользовательскими runnable

Запуск: python 06_custom_runnable.py


07_advanced_methods.py
----------------------
Дополнительные методы Runnable
Включает:
- with_retry() - повторные попытки при ошибках
- with_fallbacks() - использование альтернативных runnable
- bind() - привязка аргументов к runnable
- with_types() - привязка типов к runnable
- Комбинирование методов

Запуск: python 07_advanced_methods.py


08_complete_example.py
----------------------
Полный практический пример - валидация и регистрация пользователя
Включает:
- Простые последовательности
- Параллельная обработка
- Обработка ошибок в batch
- Использование конфигурации
- RunnableGenerator для отчетов
- Интеграция всех концепций

Запуск: python 08_complete_example.py


ИНСТРУКЦИЯ ПО ЗАПУСКУ
====================

Предварительные требования:
- Python 3.9+
- LangChain Core (установка):
  pip install langchain-core

Запуск всех примеров:
  python 01_invoke.py
  python 02_batch.py
  python 03_stream.py
  python 04_runnable_config.py
  python 05_composition.py
  python 06_custom_runnable.py
  python 07_advanced_methods.py
  python 08_complete_example.py

Или одной командой (если на Unix/Linux/macOS):
  for file in 0*.py; do python "$file" && echo ""; done


СООТВЕТСТВИЕ С МЕТОДИЧКОЙ
=========================

Раздел методички → Файлы примеров:

1. Основные концепции Runnable → 01_invoke.py, 02_batch.py

2. Методы выполнения:
   - invoke → 01_invoke.py
   - batch → 02_batch.py, 04_runnable_config.py
   - stream/astream → 03_stream.py
   - astream_events → комбинируется в 08_complete_example.py

3. Типы входа и выхода → 06_custom_runnable.py, 07_advanced_methods.py

4. RunnableConfig → 04_runnable_config.py

5. Композиция Runnable → 05_composition.py, 08_complete_example.py

6. Пользовательские Runnable → 06_custom_runnable.py

7. Дополнительные методы → 07_advanced_methods.py

8. Отладка и наблюдаемость → 04_runnable_config.py

9. Рекомендации по использованию → 08_complete_example.py


КЛЮЧЕВЫЕ КОНЦЕПЦИИ ПО ФАЙЛАМ
=============================

01_invoke.py:
- RunnableLambda(function) - оборачивание функции
- runnable.invoke(input) - вызов одного входа
- Использование config для трассировки

02_batch.py:
- runnable.batch(inputs) - параллельная обработка
- return_exceptions=True - обработка ошибок
- Измерение производительности

03_stream.py:
- runnable.stream(input) - синхронная потоковая передача
- RunnableGenerator(generator_function) - генератор
- Интеграция в конвейеры

04_runnable_config.py:
- config={'run_name': '...', 'tags': [...], ...}
- max_concurrency для ограничения параллелизма
- run_id для отслеживания запусков

05_composition.py:
- runnable_1 | runnable_2 - последовательная композиция
- runnable | {'key': runnable_2} - параллельная композиция
- runnable.pipe(other1, other2) - явная композиция

06_custom_runnable.py:
- RunnableLambda для функций
- RunnableGenerator для генераторов
- Композиция пользовательских runnable

07_advanced_methods.py:
- .with_retry(stop_after_attempt=...) - повторные попытки
- .with_fallbacks([...]) - альтернативные runnable
- .bind(param=value) - привязка аргументов
- .with_types(input_type=..., output_type=...)

08_complete_example.py:
- Все методы вместе в реальном сценарии
- Email валидация и регистрация пользователя
- Параллельная обработка
- Обработка ошибок


СОВЕТЫ ДЛЯ ИЗУЧЕНИЯ
===================

1. Начните с 01_invoke.py для понимания базики
2. Изучите 02_batch.py для параллельной обработки
3. Переходите к 05_composition.py для построения цепочек
4. Используйте 06_custom_runnable.py как справочник для своих функций
5. Применяйте методы из 07_advanced_methods.py для надежности
6. Изучите 08_complete_example.py для полного примера

Каждый файл можно запустить независимо и содержит полную демонстрацию
своего раздела методички.
"""
