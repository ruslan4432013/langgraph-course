class ToDoList:
    def __init__(self):
        # user_id → {list_name → [tasks]}
        self._lists: dict[str, dict[str, list[str]]] = {}

    def _get_user_lists(self, user_id: str) -> dict[str, list[str]]:
        """Возвращает списки конкретного пользователя."""
        if user_id not in self._lists:
            self._lists[user_id] = {}
        return self._lists[user_id]

    def init_list(self, user_id: str, name: str) -> str:
        """Создаёт новый список для пользователя."""
        user_lists = self._get_user_lists(user_id)
        if name in user_lists:
            return f"Список '{name}' уже существует"
        user_lists[name] = []
        return f"Список '{name}' создан"

    def add_task(self, user_id: str, list_name: str, task: str) -> str:
        """Добавляет задачу в список пользователя."""
        user_lists = self._get_user_lists(user_id)
        if list_name not in user_lists:
            return f"Список '{list_name}' не найден"
        user_lists[list_name].append(task)
        return f"Задача '{task}' добавлена в '{list_name}'"

    def get_lists(self, user_id: str) -> dict[str, list[str]]:
        """Возвращает все списки пользователя."""
        return self._get_user_lists(user_id)

    def get_tasks(self, user_id: str, list_name: str) -> list[str]:
        """Возвращает задачи из списка пользователя."""
        user_lists = self._get_user_lists(user_id)
        return user_lists.get(list_name, [])


to_do_list = ToDoList()
