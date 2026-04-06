class ToDoList:
    """
    Класс для работы со списками дел (ToDo).
    Все списки хранятся в оперативной памяти в словаре.
    """

    def __init__(self):
        self._lists: dict[str, list[str]] = {}

    def init_list(self, name: str):
        """Создаёт новый список дел, если его ещё нет."""
        if name in self._lists:
            raise Exception(f"Список '{name}' уже существует")
        self._lists[name] = []

    def add_task(self, name_list: str, task: str):
        """Добавляет задачу в существующий список дел."""
        self.__check_exists(name_list)
        self._lists[name_list].append(task)

    def __check_exists(self, name_list: str):
        if name_list not in self._lists:
            raise Exception(
                f"TO-DO '{name_list}' not found! "
                f"Use init_list()."
            )

    def get_lists(self) -> list[str]:
        return list(self._lists.keys())

    def get_tasks(self) -> dict[str, list[str]]:
        return dict(self._lists.items())


to_do_list = ToDoList()
