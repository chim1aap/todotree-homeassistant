"""Sample API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout


class TodotreeApiClientError(Exception):
    """Exception to indicate a general API error."""


class TodotreeApiClientCommunicationError(
    TodotreeApiClientError,
):
    """Exception to indicate a communication error."""


class TodotreeApiClientAuthError(
    TodotreeApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise TodotreeApiClientAuthError(
            msg,
        )
    response.raise_for_status()


class TodotreeApiClient:
    """Sample API Client."""

    def __init__(
        self,
        #username: str,
        #password: str,
        #session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client. TODO: Implement."""
        #self._username = username
        #self._password = password
        #self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get",
            url="https://jsonplaceholder.typicode.com/posts/1",
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise TodotreeApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise TodotreeApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise TodotreeApiClientError(
                msg,
            ) from exception



    async def create_task(self):
        """Create a task."""
        raise NotImplemented("This method is not implemented.")

    async def update_task(self):
        """Update the task."""
        raise NotImplemented("This method is not implemented.")

    async def delete_task(self):
        """Delete the task."""
        raise NotImplemented("This method is not implemented.")

    async def _get_database(self):
        """Get the list of all the tasks."""
        raise NotImplemented("This method is not implemented.")
