"""
Minimal MQTT 3.1.1 packet codec — only the packet types used by the QoS-2 flow.

Client → broker: CONNECT, PUBLISH, PUBREL, PINGREQ, DISCONNECT
Broker → client: CONNACK, PUBREC, PUBCOMP, PINGRESP
"""

import struct
import socket
import time
from dataclasses import dataclass, field
from typing import Optional


# ── packet type constants ──────────────────────────────────────────────────────
PT_CONNECT    = 1
PT_CONNACK    = 2
PT_PUBLISH    = 3
PT_PUBREC     = 5
PT_PUBREL     = 6
PT_PUBCOMP    = 7
PT_PINGREQ    = 12
PT_PINGRESP   = 13
PT_DISCONNECT = 14

PACKET_NAMES = {
    PT_CONNECT: "CONNECT", PT_CONNACK: "CONNACK",
    PT_PUBLISH: "PUBLISH", PT_PUBREC: "PUBREC",
    PT_PUBREL: "PUBREL",   PT_PUBCOMP: "PUBCOMP",
    PT_PINGREQ: "PINGREQ", PT_PINGRESP: "PINGRESP",
    PT_DISCONNECT: "DISCONNECT",
}

# map symbol names used in TRE specs to packet type IDs
SYMBOL_TO_PT = {
    "CONNECT": PT_CONNECT,   "CONNACK": PT_CONNACK,
    "PUBLISH": PT_PUBLISH,   "PUBREC": PT_PUBREC,
    "PUBREL": PT_PUBREL,     "PUBCOMP": PT_PUBCOMP,
    "PINGREQ": PT_PINGREQ,   "PINGRESP": PT_PINGRESP,
    "DISCONNECT": PT_DISCONNECT,
}

CLIENT_SYMBOLS = {"CONNECT", "PUBLISH", "PUBREL", "PINGREQ", "DISCONNECT"}
BROKER_SYMBOLS = {"CONNACK", "PUBREC", "PUBCOMP", "PINGRESP"}


# ── encoding helpers ───────────────────────────────────────────────────────────

def _encode_remaining_length(length: int) -> bytes:
    result = b""
    while True:
        byte = length % 128
        length //= 128
        if length > 0:
            byte |= 0x80
        result += bytes([byte])
        if length == 0:
            break
    return result


def _encode_str(s: str) -> bytes:
    encoded = s.encode("utf-8")
    return struct.pack("!H", len(encoded)) + encoded


# ── packet encoders ────────────────────────────────────────────────────────────

def make_connect(client_id: str = "", keepalive: int = 60,
                 clean_session: bool = True) -> bytes:
    protocol_name = _encode_str("MQTT")
    protocol_level = bytes([4])                  # MQTT 3.1.1
    connect_flags  = bytes([0x02 if clean_session else 0x00])
    ka_bytes       = struct.pack("!H", keepalive)
    ci_bytes       = _encode_str(client_id)
    payload = protocol_name + protocol_level + connect_flags + ka_bytes + ci_bytes
    return bytes([0x10]) + _encode_remaining_length(len(payload)) + payload


def make_publish(topic: str, payload: bytes, msgid: int,
                 dup: bool = False, retain: bool = False) -> bytes:
    flags  = (2 << 1) | (8 if dup else 0) | (1 if retain else 0)
    header = (PT_PUBLISH << 4) | flags
    topic_bytes  = _encode_str(topic)
    msgid_bytes  = struct.pack("!H", msgid)
    body = topic_bytes + msgid_bytes + payload
    return bytes([header]) + _encode_remaining_length(len(body)) + body


def make_pubrel(msgid: int) -> bytes:
    return bytes([0x62, 0x02]) + struct.pack("!H", msgid)


def make_pingreq() -> bytes:
    return bytes([0xC0, 0x00])


def make_disconnect() -> bytes:
    return bytes([0xE0, 0x00])


# ── packet decoder ─────────────────────────────────────────────────────────────

@dataclass
class MQTTPacket:
    ptype: int
    flags: int
    payload: bytes

    @property
    def name(self) -> str:
        return PACKET_NAMES.get(self.ptype, f"UNKNOWN({self.ptype})")

    @property
    def msgid(self) -> Optional[int]:
        """Return the 2-byte message-id if present."""
        if len(self.payload) >= 2:
            return struct.unpack("!H", self.payload[:2])[0]
        return None

    @property
    def return_code(self) -> Optional[int]:
        """CONNACK return code."""
        if self.ptype == PT_CONNACK and len(self.payload) >= 2:
            return self.payload[1]
        return None


def _read_remaining_length(sock: socket.socket) -> int:
    multiplier = 1
    value = 0
    for _ in range(4):
        byte = sock.recv(1)
        if not byte:
            raise ConnectionError("Broker closed connection while reading remaining length")
        byte = byte[0]
        value += (byte & 0x7F) * multiplier
        multiplier *= 128
        if not (byte & 0x80):
            break
    return value


def recv_packet(sock: socket.socket) -> MQTTPacket:
    """Read and decode one MQTT packet from the socket."""
    header_byte = sock.recv(1)
    if not header_byte:
        raise ConnectionError("Broker closed connection")
    header = header_byte[0]
    ptype  = (header >> 4) & 0x0F
    flags  = header & 0x0F
    remaining = _read_remaining_length(sock)
    payload = b""
    while len(payload) < remaining:
        chunk = sock.recv(remaining - len(payload))
        if not chunk:
            raise ConnectionError("Broker closed connection while reading payload")
        payload += chunk
    return MQTTPacket(ptype, flags, payload)


# ── synchronous MQTT client ────────────────────────────────────────────────────

class RawMQTTClient:
    """
    A thin synchronous MQTT client that gives full timing control.
    Every send and receive is explicit; no background threads.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 1883,
                 timeout: float = 3.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: Optional[socket.socket] = None

    # ── connection lifecycle ───────────────────────────────────────────────────

    def connect(self, client_id: str = "", keepalive: int = 60,
                clean_session: bool = True) -> MQTTPacket:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(self.timeout)
        self._sock.connect((self.host, self.port))
        self._sock.sendall(make_connect(client_id, keepalive, clean_session))
        return recv_packet(self._sock)              # CONNACK

    def disconnect(self) -> None:
        if self._sock:
            try:
                self._sock.sendall(make_disconnect())
            except OSError:
                pass
            finally:
                self._sock.close()
                self._sock = None

    # ── QoS-2 primitives ──────────────────────────────────────────────────────

    def publish_qos2(self, topic: str, payload: bytes, msgid: int,
                     dup: bool = False) -> MQTTPacket:
        """Send PUBLISH and wait for PUBREC."""
        self._sock.sendall(make_publish(topic, payload, msgid, dup=dup))
        return recv_packet(self._sock)              # PUBREC (expected)

    def pubrel(self, msgid: int) -> MQTTPacket:
        """Send PUBREL and wait for PUBCOMP."""
        self._sock.sendall(make_pubrel(msgid))
        return recv_packet(self._sock)              # PUBCOMP (expected)

    def pingreq(self) -> MQTTPacket:
        """Send PINGREQ and wait for PINGRESP."""
        self._sock.sendall(make_pingreq())
        return recv_packet(self._sock)              # PINGRESP (expected)

    # ── raw send / timed recv ─────────────────────────────────────────────────

    def send_raw(self, data: bytes) -> None:
        self._sock.sendall(data)

    def try_recv(self, timeout: float = 0.5) -> Optional[MQTTPacket]:
        old = self._sock.gettimeout()
        self._sock.settimeout(timeout)
        try:
            return recv_packet(self._sock)
        except (socket.timeout, ConnectionError):
            return None
        finally:
            self._sock.settimeout(old)
