from functools import cached_property
import json
import os
from typing import Any, ClassVar
from urllib.parse import urljoin

from dotenv import load_dotenv
import httpx

from app.types import SimpleJSON
from diadoc.exceptions import DiadocHTTPException

load_dotenv()


class DiadocHTTP:
    diadoc_base_url: ClassVar[str] = "https://diadoc-api.kontur.ru/"

    @cached_property
    def token(self) -> str:
        return self.post(
            url="/v3/Authenticate?type=password",
            headers=self.get_base_headers(),
            payload={
                "login": os.getenv("DIADOC_LOGIN"),
                "password": os.getenv("DIADOC_PASSWORD"),
            },
            expects_json=False,
        )  # type: ignore

    @cached_property
    def headers(self) -> dict[str, str]:
        headers = self.get_base_headers()
        headers["Authorization"] += f",ddauth_token={self.token}"
        return headers

    def request(
        self,
        url: str,
        method: str,
        headers: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        expected_status_code: int = 200,
        expects_json: bool = True,
    ) -> SimpleJSON | str:
        if headers is None:
            headers = self.headers

        response = httpx.request(
            url=self.format_url(url),
            method=method,
            headers=headers,
            params=params,
            json=payload,
        )

        self.raise_if_error_occurred(response, expected_status_code)

        if expects_json:
            return self.get_response_json(response)

        return response.text

    def get(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        expected_status_code: int = 200,
        expects_json: bool = True,
    ) -> SimpleJSON | str:
        return self.request(
            url,
            method="GET",
            headers=headers,
            params=params,
            payload=payload,
            expected_status_code=expected_status_code,
            expects_json=expects_json,
        )

    def post(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        expected_status_code: int = 200,  # diadoc return 200 on POST
        expects_json: bool = True,
    ) -> SimpleJSON | str:
        return self.request(
            url,
            "POST",
            headers=headers,
            params=params,
            payload=payload,
            expected_status_code=expected_status_code,
            expects_json=expects_json,
        )

    def format_url(self, url: str) -> str:
        return urljoin(self.diadoc_base_url, url.strip("/"))

    def get_base_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f'DiadocAuth ddauth_api_client_id={os.getenv("DIADOC_CLIENT_ID")}',
        }

    def raise_if_error_occurred(self, response: httpx.Response, expected_status_code: int) -> None:
        if response.status_code != expected_status_code:
            raise DiadocHTTPException(
                code=response.status_code,
                message=f"HTTP Error {response.status_code}, fetched url '{response.url}', {response.text}",
            )

    def get_response_json(self, response: httpx.Response) -> SimpleJSON:
        try:
            return response.json()
        except json.JSONDecodeError as decode_error:
            raise DiadocHTTPException(
                code=response.status_code,
                message=f"JSON decode error {decode_error}, fetched url '{response.url}, {response.text}'",
            )
