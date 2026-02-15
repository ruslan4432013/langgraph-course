from src.server import mcp
from src.service.to_do_list import to_do_list

# Примеры старых текстовых ресурсов (закомментированы)
# @mcp.resource("to-do://lists", mime_type="text/plain")
# def show_lists() -> str:
#     """
#         Получает все списки дел.
#
#         Возвращает:
#             str: Все списки через точку с запятой.
#     """
#     tasks = to_do_list.get_lists()
#     return "; ".join(tasks)
#
# @mcp.resource("to-do://lists/{name}", mime_type="text/plain")
# def show_list(name: str) -> str:
#     """
#         Получает все задачи из указанного списка дел.
#
#         Аргументы:
#             name (str): Имя списка дел для получения задач.
#
#         Возвращает:
#             str: Все задачи списка через точку с запятой.
#     """
#     tasks = to_do_list.find_list(name)
#     return "; ".join(tasks)


# Структурированный вывод

@mcp.resource("to-do://lists", mime_type="application/json")
def show_lists() -> list[str]:
    """
        Получает все списки дел.

        Возвращает:
            list[str]: Список всех названий списков дел.
    """
    return to_do_list.get_lists()


@mcp.resource("to-do://tasks", mime_type="application/json")
def show_tasks() -> dict[str, list[str]]:
    """
        Получает все задачи из всех списков дел.

        Возвращает:
            dict[str, list[str]]: Словарь, где ключ — имя списка дел,
            а значение — список задач в этом списке.
    """
    return to_do_list.get_tasks()
