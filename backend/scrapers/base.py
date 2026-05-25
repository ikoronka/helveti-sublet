import asyncio
import time
import httpx


class BaseScraper:
    SOURCE = ""
    RATE_LIMIT = 10  # requests per minute

    def __init__(self):
        self._request_times: list[float] = []
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            headers={"User-Agent": "HelvetiSublet/1.0"},
            timeout=15.0,
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, *args):
        if self._client:
            await self._client.aclose()

    async def _get(self, url: str, params: dict | None = None) -> dict | list:
        await self._throttle()
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def _throttle(self):
        now = time.monotonic()
        self._request_times = [t for t in self._request_times if now - t < 60]
        if len(self._request_times) >= self.RATE_LIMIT:
            sleep_for = 60 - (now - self._request_times[0]) + 0.1
            await asyncio.sleep(sleep_for)
        self._request_times.append(time.monotonic())

    async def scrape(self) -> list[dict]:
        raise NotImplementedError
