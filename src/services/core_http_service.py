from abc import ABC
from typing import Any

from aiohttp import ClientSession


class BaseHTTPService(ABC):

    @staticmethod
    async def execute_request(
            url: str,
            body: dict[str, Any],
            url_params: dict[str, Any] | None = None,
            headers: dict[str, Any] | None = None,
            method: str = "GET"
    ):
        """
        Выполняет HTTP-запрос с обработкой токена и ошибок JSON-декодирования.
        """
        if headers is None:
            headers = {
                "Content-Type": "application/json",
            }

        async with ClientSession() as session:
            response_data, status = await BaseHTTPService.make_request(
                session, url, method, body, url_params, headers
            )

        return response_data, status