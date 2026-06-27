import asyncio
import websockets
import json
import random
from websockets.exceptions import (
    ConnectionClosedError,
    ConnectionClosedOK,
    WebSocketException,
)


class ExponentialBackoff:
    def __init__(self, base=1, max=60, jitter=0.3):
        self.base = base
        self.max = max
        self.jitter = jitter
        self.attempts = 0

    def next_delay(self):
        delay = min(self.max, self.base * (2**self.attempts))
        delay += random.uniform(0, self.jitter)
        self.attempts += 1
        return delay

    def reset_delay(self):
        self.attempts = 0


class PersistentWebSocketClient:
    def __init__(
        self, uri, message_handler, ping_interval=30, ping_timeout=10, extra_headers={}
    ):
        self.uri = uri
        self.message_handler = message_handler
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.extra_headers = extra_headers
        self.__backoff = ExponentialBackoff(1, 60, 0.3)
        self.__running = False
        self.__ws = None

    async def start(self):
        self.__running = True
        await self._connection_loop()

    async def stop(self):
        self.__running = False
        if self.__ws:
            await self.__ws.close()

    async def send(self, message):
        if self.__ws:
            if isinstance(message, dict):
                message = json.dumps(message)
            await self.__ws.send(message)
        else:
            raise ConnectionError("WebSocket is not connected.")

    async def _connection_loop(self):
        while self.__running:
            try:
                await self._connect_and_listen()
            except ConnectionClosedOK:
                # Server closed cleanly (1000) — could be intentional
                print("Server closed connection cleanly")
                if not self._running:
                    break  # we called stop(), exit
                # still reconnect — server may restart

            except (ConnectionClosedError, WebSocketException) as exc:
                print(f"Connection error: {exc}")

            except (OSError, ConnectionRefusedError) as exc:
                # Network-level failure (DNS, TCP refused, etc.)
                print(f"Network error: {exc}")

            except Exception as exc:
                print(f"Unexpected error in listener: {exc}")

            if not self._running:
                break
            delay = self._backoff.next()
            print(f"Reconnecting in {delay:.1f}s (attempt #{self._backoff.attempt})")
            await asyncio.sleep(delay)

        return

    async def _connect_and_listen(self):
        async with websockets.connect(
            self.uri,
            ping_interval=self.ping_interval,
            ping_timeout=self.ping_timeout,
            additional_headers=self.extra_headers,
            open_timeout=10,
            close_timeout=10,
        ) as ws:
            self.__ws = ws
            self.__backoff.reset_delay()
            async for message in self.__ws:
                if not self.__running:
                    break
            try:
                await self.message_handler(message)
            except Exception as e:
                print(f"Error in message handler: {e}")
        self.__ws = None

    async def _on_connect(self, ws):
        """
        Override this to send a subscription message after connecting.
        e.g. Binance, Coinbase, Kraken all require you to send a JSON
        subscribe frame after the WS handshake completes.
        """
        pass
