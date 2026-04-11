import webbrowser
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pydantic import AnyUrl
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.shared.auth import OAuthClientInformationFull, OAuthClientMetadata, OAuthToken
from src.settings import settings

class InMemoryTokenStorage(TokenStorage):
    """Хранилище токенов в памяти."""

    def __init__(self):
        self._tokens: OAuthToken | None = None
        self._client_info: OAuthClientInformationFull | None = None

    async def get_tokens(self) -> OAuthToken | None:
        return self._tokens

    async def set_tokens(self, tokens: OAuthToken) -> None:
        self._tokens = tokens

    async def get_client_info(self) -> OAuthClientInformationFull | None:
        return self._client_info

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        self._client_info = client_info

_callback_data: dict = {"code": None, "state": None, "error": None}


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)

        if "error" in params:
            _callback_data["error"] = params["error"][0]
            self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"Ошибка: {_callback_data['error']}".encode())
            return

        _callback_data["code"] = params.get("code", [None])[0]
        _callback_data["state"] = params.get("state", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("Авторизация успешна! Вернитесь в терминал.".encode())

    def log_message(self, format, *args):
        pass


def _start_callback_server() -> HTTPServer:
    parsed = urlparse(settings.CALLBACK_URL)
    port = parsed.port or 80
    server = HTTPServer(("localhost", port), _CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def create_oauth_provider() -> OAuthClientProvider:
    """
    Создаёт OAuthClientProvider из MCP SDK.

    Он сам делает: discovery, DCR, PKCE, обмен code→token, refresh.
    Это httpx.Auth — передаётся в MultiServerMCPClient через параметр auth.
    """
    server = _start_callback_server()

    async def redirect_handler(authorization_url: str) -> None:
        print("=" * 50)
        print("Открываем браузер для входа через GitHub...")
        print(f"Если браузер не открылся:")
        print(f"  {authorization_url}")
        print("=" * 50)
        webbrowser.open(authorization_url)

    async def callback_handler() -> tuple[str, str | None]:
        start = time.time()
        while time.time() - start < 120:
            if _callback_data["code"]:
                server.shutdown()
                return _callback_data["code"], _callback_data["state"]
            if _callback_data["error"]:
                server.shutdown()
                raise ValueError(f"OAuth ошибка: {_callback_data['error']}")
            time.sleep(0.1)
        server.shutdown()
        raise TimeoutError("Таймаут ожидания авторизации (2 мин)")

    return OAuthClientProvider(
        server_url=f"{settings.MCP_SERVER_URL}/mcp",
        client_metadata=OAuthClientMetadata(
            client_name="MCP ToDo Client",
            redirect_uris=[AnyUrl(settings.CALLBACK_URL)],
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
        ),
        storage=InMemoryTokenStorage(),
        redirect_handler=redirect_handler,
        callback_handler=callback_handler,
    )
