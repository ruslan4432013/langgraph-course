import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict, Optional

_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "to_do_list.json"


class TaskEntry(TypedDict):
    title: str
    created_at: str


class ListEntry(TypedDict):
    created_at: str
    tasks: list[TaskEntry]


class Storage:
    """Отвечает за чтение и запись данных в JSON файл."""

    def __init__(self, data_file: Path = _DATA_FILE):
        self._data_file = data_file
        self._data_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, ListEntry]:
        if not self._data_file.exists():
            return {}
        with open(self._data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data: dict[str, ListEntry]) -> None:
        with open(self._data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def now() -> str:
        return datetime.now(timezone.utc).isoformat()


class ToDoList:
    """Управляет списками дел. Ключи — только ASCII символы."""

    def __init__(self, storage: Storage | None = None):
        self._storage = storage or Storage()

    def init_list(self, key: str) -> None:
        """Создаёт новый список дел. Если список уже существует — ничего не делает."""
        self._validate_key(key)
        data = self._storage.load()
        if key in data:
            return
        data[key] = {"created_at": self._storage.now(), "tasks": []}
        self._storage.save(data)

    def add_task(self, key: str, title: str) -> None:
        """Добавляет задачу в существующий список."""
        data = self._storage.load()
        self._check_exists(data, key)
        data[key]["tasks"].append({"title": title, "created_at": self._storage.now()})
        self._storage.save(data)

    def get_lists(self) -> list[str]:
        return list(self._storage.load().keys())

    def get_tasks(self, key: Optional[str] = None) -> dict[str, list[TaskEntry]]:
        data = self._storage.load()
        if key is not None:
            if key not in data:
                return {}
            return {key: data[key]["tasks"]}
        return {k: entry["tasks"] for k, entry in data.items()}

    @staticmethod
    def _validate_key(key: str) -> None:
        if not key.isascii() or not key.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                f"List key '{key}' must contain only ASCII letters, digits, hyphens or underscores"
            )

    @staticmethod
    def _check_exists(data: dict, key: str) -> None:
        if key not in data:
            raise KeyError(f"List '{key}' not found. Use init_list() first.")


to_do_list = ToDoList()

if __name__ == '__main__':
    print(to_do_list.get_tasks())
