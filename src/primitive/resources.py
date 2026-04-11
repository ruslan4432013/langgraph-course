import json
from server import mcp
from src.service.to_do_list import to_do_list

@mcp.resource("to-do://lists", mime_type="application/json")
def show_lists() -> str:
    """
        Получает все списки дел всех пользователей.

        Возвращает:
            str: JSON-словарь, где ключ — "{user_id}/{имя_списка}",
            а значение — список задач.

        Примечание: без контекста запроса ресурс возвращает все данные.
        В реальном приложении ресурсы тоже должны быть защищены.
    """
    all_lists = {}
    for user_id, user_lists in to_do_list._lists.items():
        for name, tasks in user_lists.items():
            all_lists[f"{user_id}/{name}"] = tasks

    return json.dumps(all_lists, ensure_ascii=False)
