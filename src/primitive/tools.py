from fastmcp import Context
from fastmcp.server.auth import AccessToken
from fastmcp.dependencies import CurrentAccessToken
from server import mcp
from src.service.to_do_list import to_do_list

@mcp.tool(title="Создать список")
async def init_to_do_list(
    name_list: str,
    ctx: Context,
    token: AccessToken = CurrentAccessToken(),
) -> str:
    """
        Создаёт новый список дел с указанным именем.

        Аргументы:
            name_list (str): Имя нового списка дел.
            token (AccessToken): OAuth-токен пользователя (внедряется автоматически).

        Возвращает:
            str: Сообщение о статусе, подтверждающее создание или объясняющее ошибку.
    """
    # Получаем user_id из OAuth-токена
    user_id = token.claims.get("sub", "anonymous")
    await ctx.info(f"[{user_id}] Создание списка '{name_list}'")

    result = to_do_list.init_list(user_id, name_list)
    await ctx.info(f"[{user_id}] {result}")
    return result


@mcp.tool(title="Добавить задачу")
async def add_task_to_do_list(
    list_name: str,
    task: str,
    ctx: Context,
    token: AccessToken = CurrentAccessToken(),
) -> str:
    """
        Добавляет задачу в существующий список дел.

        Аргументы:
            list_name (str): Имя списка дел, в который будет добавлена задача.
            task (str): Задача для добавления.
            token (AccessToken): OAuth-токен пользователя (внедряется автоматически).

        Возвращает:
            str: Сообщение о статусе, подтверждающее добавление или объясняющее ошибку.
    """
    # Получаем user_id из OAuth-токена
    user_id = token.claims.get("sub", "anonymous")
    await ctx.debug(f"[{user_id}] Добавление задачи '{task}' в '{list_name}'")

    result = to_do_list.add_task(user_id, list_name, task)
    await ctx.info(f"[{user_id}] {result}")
    return result


@mcp.tool(title="Показать задачи")
async def get_tasks(
    list_name: str,
    ctx: Context,
    token: AccessToken = CurrentAccessToken(),
) -> str:
    """
        Возвращает задачи из указанного списка дел.

        Аргументы:
            list_name (str): Имя списка дел.
            token (AccessToken): OAuth-токен пользователя (внедряется автоматически).

        Возвращает:
            str: Список задач или сообщение о том, что список пуст/не найден.
    """
    # Получаем user_id из OAuth-токена
    user_id = token.claims.get("sub", "anonymous")

    tasks = to_do_list.get_tasks(user_id, list_name)
    if not tasks:
        return f"Список '{list_name}' пуст или не найден"

    return "\n".join(f"- {task}" for task in tasks)
