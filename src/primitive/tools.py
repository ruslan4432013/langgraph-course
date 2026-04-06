from enum import Enum

from fastmcp import Context
from pydantic import BaseModel, Field

from src.server import mcp
from src.service.to_do_list import to_do_list


# --- Модели для эликитации ---

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskDetails(BaseModel):
    task: str = Field(description="Описание задачи")
    priority: Priority = Field(default=Priority.MEDIUM, description="Приоритет")


# --- Инструменты ---

@mcp.tool()
async def init_to_do_list(name_list: str, ctx: Context) -> str:
    """
        Создаёт новый список дел с указанным именем.

        Аргументы:
            name_list (str): Имя нового списка дел.

        Возвращает:
            str: Сообщение о статусе, подтверждающее создание или объясняющее ошибку.
    """
    await ctx.info(f"Запрос на создание списка: '{name_list}'")

    # Эликитация: запрашиваем подтверждение у пользователя
    result = await ctx.elicit(
        message=f"Вы уверены, что хотите создать список '{name_list}'?",
        response_type=None,  # Только подтверждение, без данных
    )

    if result.action != "accept":
        await ctx.warning("Создание списка отменено пользователем")
        return "Создание списка отменено"

    if name_list in to_do_list.get_lists():
        await ctx.warning(f"Список '{name_list}' уже существует")
        return f"Список '{name_list}' уже существует"

    to_do_list.init_list(name_list)
    await ctx.info(f"Список '{name_list}' успешно создан")
    return f"TO-DO #{name_list} создан."


@mcp.tool()
async def add_task_to_do_list(task: str, list_name: str, ctx: Context) -> str:
    """
        Добавляет задачу в существующий список дел.

        Аргументы:
            task (str): Задача для добавления.
            list_name (str): Имя списка дел, в который будет добавлена задача.

        Возвращает:
            str: Сообщение о статусе, подтверждающее добавление или объясняющее ошибку.
    """
    await ctx.debug(f"Добавление задачи '{task}' в список '{list_name}'")

    if list_name not in to_do_list.get_lists():
        await ctx.error(f"Список '{list_name}' не найден")
        return f"Список '{list_name}' не найден"

    to_do_list.add_task(list_name, task)
    await ctx.info(f"Задача добавлена в '{list_name}'")
    return f"Задача '{task}' добавлена в список '{list_name}'"


@mcp.tool()
async def add_detailed_task(list_name: str, ctx: Context) -> str:
    """
        Добавляет задачу с приоритетом в список дел.
        Запрашивает у пользователя детали задачи через эликитацию.

        Аргументы:
            list_name (str): Имя списка дел.

        Возвращает:
            str: Сообщение о результате операции.
    """
    await ctx.info(f"Добавление задачи в список '{list_name}'")

    if list_name not in to_do_list.get_lists():
        await ctx.error(f"Список '{list_name}' не найден")
        return f"Список '{list_name}' не найден"

    # Эликитация: запрашиваем структурированные данные
    result = await ctx.elicit(
        message=f"Заполните детали задачи для списка '{list_name}':",
        response_type=TaskDetails,
    )

    if result.action == "accept":
        task_data = result.data
        to_do_list.add_task(list_name, f"[{task_data.priority.value}] {task_data.task}")
        await ctx.info(f"Задача '{task_data.task}' добавлена с приоритетом {task_data.priority.value}")
        return f"Задача '{task_data.task}' (приоритет: {task_data.priority.value}) добавлена в '{list_name}'"
    elif result.action == "decline":
        return "Пользователь отказался добавлять задачу"
    else:
        return "Операция отменена"


@mcp.tool()
async def generate_tasks(list_name: str, topic: str, ctx: Context) -> str:
    """
        Генерирует задачи для списка с помощью LLM клиента (сэмплирование).

        Аргументы:
            list_name (str): Имя списка дел.
            topic (str): Тема, по которой нужно сгенерировать задачи.

        Возвращает:
            str: Список сгенерированных и добавленных задач.
    """
    await ctx.info(f"Генерация задач для '{list_name}' по теме '{topic}'")

    if list_name not in to_do_list.get_lists():
        await ctx.error(f"Список '{list_name}' не найден")
        return f"Список '{list_name}' не найден"

    # Сэмплирование: запрашиваем у клиента LLM-генерацию
    result = await ctx.sample(
        messages=f"Придумай 3 конкретные задачи по теме '{topic}'. "
                 f"Верни только список задач, по одной на строку, без нумерации.",
        system_prompt="Ты помощник для составления списков дел. Отвечай кратко.",
        max_tokens=200,
    )

    generated_text = result.text or ""
    tasks = [t.strip() for t in generated_text.strip().split("\n") if t.strip()]

    for task in tasks:
        to_do_list.add_task(list_name, task)
        await ctx.info(f"Добавлена задача: {task}")

    return f"Добавлено {len(tasks)} задач в список '{list_name}':\n" + "\n".join(tasks)
