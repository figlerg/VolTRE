"""
Replay harness: translates a VolTRE TimedWord into an MQTT interaction and
records the broker's responses.

The timed word contains CLIENT events only (CONNECT, PUBLISH, PUBREL,
PINGREQ, DISCONNECT).  Broker responses (CONNACK, PUBREC, PUBCOMP, PINGRESP)
are awaited after each matching client send; unexpected or missing responses
are flagged as conformance violations.
"""

import socket
import time
from dataclasses import dataclass, field
from typing import Optional

from mqtt_codec import (
    RawMQTTClient, MQTTPacket,
    PT_CONNACK, PT_PUBREC, PT_PUBCOMP, PT_PINGRESP, PT_DISCONNECT,
    make_connect, make_publish, make_pubrel, make_pingreq, make_disconnect,
    PACKET_NAMES,
)


# ── expected broker responses ──────────────────────────────────────────────────

EXPECTED_RESPONSE = {
    "CONNECT":    PT_CONNACK,
    "PUBLISH":    PT_PUBREC,
    "PUBREL":     PT_PUBCOMP,
    "PINGREQ":    PT_PINGRESP,
    "DISCONNECT": None,           # no response expected
}


# ── result types ───────────────────────────────────────────────────────────────

@dataclass
class InteractionEvent:
    timestamp: float
    direction: str      # "send" | "recv"
    symbol: str
    msgid: Optional[int] = None
    details: str = ""


@dataclass
class ReplayResult:
    timed_word: object                                 # TimedWord
    events: list = field(default_factory=list)        # list[InteractionEvent]
    conformance_violations: list = field(default_factory=list)   # list[str]
    exception: Optional[Exception] = None
    completed: bool = False

    @property
    def ok(self) -> bool:
        return self.completed and not self.conformance_violations and self.exception is None

    def __str__(self) -> str:
        status = "OK" if self.ok else "FAIL"
        viols  = "; ".join(self.conformance_violations) if self.conformance_violations else "none"
        exc    = repr(self.exception) if self.exception else "none"
        return (f"ReplayResult({status}  violations={viols}  exc={exc}  "
                f"events={len(self.events)})")


# ── replay ─────────────────────────────────────────────────────────────────────

def replay(
    timed_word,
    host:        str   = "127.0.0.1",
    port:        int   = 18830,
    topic:       str   = "test/fuzz",
    msgid:       int   = 1,
    payload:     bytes = b"fuzz",
    timeout:     float = 3.0,
    delay_scale: float = 1.0,
) -> ReplayResult:
    """
    delay_scale: multiply all delays by this factor before sleeping.
    Set < 1.0 to compress timing for fast local testing (e.g. 0.05 makes a
    30-second trace run in 1.5 seconds while preserving the event ordering).
    """
    """
    Replay a timed word against an MQTT broker.

    The word contains only client-side symbols.  After each symbol we wait up
    to `timeout` seconds for the broker's expected response and record whether
    it arrived.

    Multiple PUBLISH symbols in the same word all use the same msgid (the
    default is 1), which is the minimal trigger for CVE-2023-28366-style bugs.
    """

    result   = ReplayResult(timed_word=timed_word)
    client   = RawMQTTClient(host=host, port=port, timeout=timeout)
    t0       = time.monotonic()
    connected = False

    def log_send(symbol: str, mid: Optional[int] = None) -> None:
        result.events.append(InteractionEvent(
            timestamp=time.monotonic() - t0,
            direction="send",
            symbol=symbol,
            msgid=mid,
        ))

    def log_recv(pkt: Optional[MQTTPacket], expected_pt: int) -> None:
        if pkt is None:
            sym = "TIMEOUT"
            result.conformance_violations.append(
                f"Expected {PACKET_NAMES.get(expected_pt,'?')} but got timeout"
            )
        else:
            sym = pkt.name
            if pkt.ptype != expected_pt:
                result.conformance_violations.append(
                    f"Expected {PACKET_NAMES.get(expected_pt,'?')} but got {pkt.name}"
                )
        result.events.append(InteractionEvent(
            timestamp=time.monotonic() - t0,
            direction="recv",
            symbol=sym,
        ))

    try:
        first_connect = True
        for symbol, delay in timed_word:
            time.sleep(delay * delay_scale)

            if symbol == "CONNECT":
                log_send(symbol)
                if first_connect:
                    # First CONNECT: open TCP connection
                    pkt = client.connect(keepalive=60, clean_session=True)
                    log_recv(pkt, PT_CONNACK)
                    connected = True
                    first_connect = False
                    if pkt and pkt.return_code != 0:
                        result.conformance_violations.append(
                            f"CONNACK returned non-zero code: {pkt.return_code}"
                        )
                else:
                    # Subsequent CONNECT on existing connection — MQTT 3.1.1 s.3.1.4
                    # requires the broker to disconnect; we send the packet and expect nothing.
                    client._sock.sendall(make_connect(keepalive=60, clean_session=True))
                    pkt = client.try_recv(timeout=1.0)
                    if pkt is None:
                        result.conformance_violations.append(
                            "Mid-session CONNECT: broker did not disconnect (MQTT-3.1.0-2 violation)"
                        )
                    else:
                        log_recv(pkt, PT_CONNACK)   # some brokers send CONNACK anyway

            elif symbol == "PUBLISH":
                log_send(symbol, mid=msgid)
                client._sock.sendall(make_publish(topic, payload, msgid))
                pkt = client.try_recv(timeout=timeout)
                log_recv(pkt, PT_PUBREC)

            elif symbol == "PUBREL":
                if client._sock is None:
                    result.conformance_violations.append(
                        "PUBREL attempted on closed connection (DISCONNECT occurred earlier)"
                    )
                    break
                log_send(symbol, mid=msgid)
                client._sock.sendall(make_pubrel(msgid))
                pkt = client.try_recv(timeout=timeout)
                log_recv(pkt, PT_PUBCOMP)

            elif symbol == "PINGREQ":
                if client._sock is None:
                    break
                log_send(symbol)
                client._sock.sendall(make_pingreq())
                pkt = client.try_recv(timeout=timeout)
                log_recv(pkt, PT_PINGRESP)

            elif symbol == "DISCONNECT":
                log_send(symbol)
                client.disconnect()
                connected = False

        result.completed = True

    except ConnectionError as exc:
        result.exception = exc

    except socket.timeout as exc:
        result.exception = exc

    except Exception as exc:
        result.exception = exc

    finally:
        if connected:
            client.disconnect()

    return result
