import sys
from pathlib import Path

# При запуске файла напрямую (python server/main.py) Python автоматически добавляет
# server/ в sys.path[0]. Это мешает импортировать 'server' как пакет.
# Решение: добавляем корень проекта и убираем server/ из sys.path.
_project_root = str(Path(__file__).resolve().parent.parent.parent)
_server_dir = str(Path(__file__).resolve().parent)
sys.path.insert(0, _project_root)
while _server_dir in sys.path:
    sys.path.remove(_server_dir)

from src.server.server import mcp
from src.server.primitive import tools, resources, prompts  # noqa: F401 — регистрация инструментов, ресурсов и промптов

if __name__ == "__main__":
    # SSE (Server-Sent Events) устарел. Используем Streamable HTTP транспорт.
    mcp.run(transport="streamable-http")
