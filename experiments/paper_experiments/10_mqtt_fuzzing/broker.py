"""
amqtt broker management.  Runs the broker in a background asyncio thread so the
fuzzer can connect to it with a plain synchronous socket client.
"""

import asyncio
import os
import threading
import time
import psutil
from dataclasses import dataclass, field
from typing import Optional


# ── default config ─────────────────────────────────────────────────────────────

def _broker_config(host: str, port: int) -> dict:
    return {
        "listeners": {
            "default": {
                "type": "tcp",
                "bind": f"{host}:{port}",
            }
        },
        "sys_interval": 0,
        "auth": {"allow-anonymous": True},
        "topic_check": {"enabled": False},
    }


# ── broker thread ──────────────────────────────────────────────────────────────

class BrokerThread:
    """
    Wraps an amqtt Broker running in a dedicated asyncio event loop on a
    background daemon thread.  The fuzzer interacts with the broker via plain
    TCP sockets, so no asyncio is needed on the caller side.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 18830):
        self.host = host
        self.port = port
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._broker = None
        self._thread: Optional[threading.Thread] = None
        self._ready = threading.Event()
        self._error: Optional[Exception] = None
        self._pid = os.getpid()          # broker runs in our process

    # ── public API ────────────────────────────────────────────────────────────

    def start(self, timeout: float = 10.0) -> None:
        self._thread = threading.Thread(target=self._run, daemon=True,
                                        name="amqtt-broker")
        self._thread.start()
        if not self._ready.wait(timeout=timeout):
            raise RuntimeError("amqtt broker did not start within timeout")
        if self._error:
            raise self._error

    def stop(self, timeout: float = 5.0) -> None:
        if self._loop and self._broker:
            future = asyncio.run_coroutine_threadsafe(
                self._broker.shutdown(), self._loop
            )
            try:
                future.result(timeout=timeout)
            except Exception:
                pass
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join(timeout=timeout)

    def restart(self) -> None:
        """Stop and restart the broker to get a clean session state."""
        self.stop()
        self._ready.clear()
        self._error = None
        self.start()

    @property
    def memory_rss(self) -> int:
        """Resident set size of the whole process (broker + fuzzer) in bytes."""
        return psutil.Process(self._pid).memory_info().rss

    # ── internal ──────────────────────────────────────────────────────────────

    def _run(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._start_broker())
            self._loop.run_forever()
        except Exception as exc:
            self._error = exc
            self._ready.set()
        finally:
            self._loop.close()

    async def _start_broker(self) -> None:
        from amqtt.broker import Broker
        cfg = _broker_config(self.host, self.port)
        self._broker = Broker(cfg)
        await self._broker.start()
        self._ready.set()


# ── convenience context manager ────────────────────────────────────────────────

class managed_broker:
    def __init__(self, host: str = "127.0.0.1", port: int = 18830):
        self.broker = BrokerThread(host=host, port=port)

    def __enter__(self) -> BrokerThread:
        self.broker.start()
        return self.broker

    def __exit__(self, *_) -> None:
        self.broker.stop()
