import json

from src.server import mcp
from src.service.to_do_list import to_do_list


@mcp.resource("to-do://lists", mime_type="application/json")
def show_lists() -> str:
    """
        Получает все списки дел.

        Возвращает:
            str: JSON-список всех названий списков дел.
    """
    return json.dumps(to_do_list.get_lists(), ensure_ascii=False)


@mcp.resource("to-do://tasks", mime_type="application/json")
def show_tasks() -> str:
    """
        Получает все задачи из всех списков дел.

        Возвращает:
            str: JSON-словарь, где ключ — имя списка дел,
            а значение — список задач в этом списке.
    """
    return json.dumps(to_do_list.get_tasks(), ensure_ascii=False)
