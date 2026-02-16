from dataclasses import dataclass
from typing import Literal, TypedDict
from src.server import mcp
from src.service.to_do_list import to_do_list


@mcp.tool()
def init_to_do_list(name_list: str) -> str:
    """
        Создаёт новый список дел с указанным именем.

        Аргументы:
            name_list (str): Имя нового списка дел.

        Возвращает:
            str: Сообщение о статусе, подтверждающее создание или объясняющее ошибку.
    """
    to_do_list.init_list(name_list)
    return f"TO-DO #{name_list} создан."

@mcp.tool()
def add_task_to_do_list(task: str, list_name: str) -> str:
    """
        Добавляет задачу в существующий список дел.

        Аргументы:
            task (str): Задача для добавления.
            list_name (str): Имя списка дел, в который будет добавлена задача.

        Возвращает:
            str: Сообщение о статусе, подтверждающее добавление или объясняющее ошибку.
    """
    to_do_list.add_task(list_name, task)
    return f"Задача {task} добавлена."



# Структурированный вывод

# @dataclass           # Пример с pydantic
# class Status:
#     """ Информация о создании списка """
#     status: Literal['created', 'failed']  # Статус операции: создан или ошибка
#     message: str  # Сообщение о результате
#
# @mcp.tool()
# def init_to_do_list(name_list: str) -> Status:
#     """
#         Создаёт новый список дел с указанным именем.
#
#         Аргументы:
#             name_list (str): Имя нового списка дел.
#
#         Возвращает:
#             StatusCreated: Информация о создании списка.
#     """
#     to_do_list.init_list(name_list)
#     return Status(status="created", message=f"Список дел '{name_list}' создан")
#
#
#
# class Task(TypedDict):   # Пример с TypedDict
#     status: Literal['added', 'failed']  # Статус операции: добавлено или ошибка
#     message: str  # Сообщение о результате
#
# @mcp.tool()
# def add_task_to_do_list(task: str, list_name: str) -> Task:
#     """
#         Добавляет задачу в существующий список дел.
#
#         Аргументы:
#             task (str): Задача для добавления.
#             list_name (str): Имя списка дел, в который будет добавлена задача.
#
#         Возвращает:
#             Task: Статус операции и сообщение о результате.
#     """
#     to_do_list.add_task(list_name, task)
#     print(f"Задача '{task}' добавлена в список '{list_name}'")
#     return {"status": "added", "message": f"Задача '{task}' добавлена в список '{list_name}'"}
