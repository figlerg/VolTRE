# MQTT Fuzzing Case Study: Timed Regular Expressions (TRE) Candidates

This document outlines known issues, race conditions, and timing anomalies in popular MQTT implementations (such as Mosquitto and amqtt). These candidates are specifically selected for state-and-timing fuzzing using a TRE (Timed Regular Expressions) uniform sampling tool, where the broker's state machine desynchronizes due to interleaving, race conditions, or specific delays.

## 1. The Disconnect-Before-Loop-Stop Race Condition
* **Target:** `libmosquitto` (Client library side)
* **Source:** [Mosquitto GitHub Issue #3207](https://github.com/eclipse/mosquitto/issues/3207)
* **Concept:** A race condition between an asynchronous event processing loop thread and the main controlling thread.

### Discrete Event Sequence & Timing
1. `mosquitto_loop_start`
2. `mosquitto_connect_async`
3. `CALLBACK_CONNECTED`
4. `mosquitto_disconnect`
5. `mosquitto_loop_stop`

**The Timing Hazard:** If the delay between step 4 (`disconnect`) and step 5 (`loop_stop`) is infinitesimally small, the spawned worker thread sets its internal state and exits before the main thread runs its safety checks in `loop_stop`. This causes `loop_stop` to throw an invalid error code (`MOSQ_ERR_INVAL`) and abandon the thread without joining it, leading to a resource leak.

**TRE Fuzzing Value:** The tool can model the inter-arrival time Δt between `disconnect` and `loop_stop`. Uniformly sampling tight Δt → 0 spaces should trigger the unjoined thread leak.

---

## 2. Real-Time vs. Monotonic Clock Jumps (Broker Eviction)
* **Target:** `mosquitto` (Broker daemon)
* **Source:** [Mosquitto GitHub Issue #3238](https://github.com/eclipse/mosquitto/issues/3238) (Fixed in 2.0.22)
* **Concept:** The broker's core loop failed to initialize a monotonic clock, defaulting to the system's Real-Time Clock (RTC).

### Discrete Event Sequence & Timing
1. `CLIENT_CONNECT` (KeepAlive set to T_ka seconds)
2. `PINGREQ` from client (keeps connection alive)
3. System clock adjustment/NTP sync (Time jumps forward by > T_ka)

**The Timing Hazard:** Because the broker evaluates timeouts using absolute time instead of monotonic time, a sudden discrete system time jump forward tricks the broker into thinking the client has been silent for longer than T_ka. It immediately drops the connection (`spurious disconnect`).

**TRE Fuzzing Value:** Simulating environment timing events (like NTP clock adjustments) alongside protocol events provides a unique mixed-domain timed event test case.

---

## 3. Simultaneous Client-ID Takeover Interleaving
* **Target:** Protocol-wide (Highly visible in async architectures like `amqtt`)
* **Concept:** The MQTT specification dictates that if a client connects with an ID that is already in use, the broker must disconnect the old client and accept the new one. A race condition occurs when a single client attempts to connect multiple times in rapid succession, or two clients fight for the same ID.

### Discrete Event Sequence & Timing
1. `CONNECT` (ClientID: `X`, Conn_Index: 1)
2. `CONNECT` (ClientID: `X`, Conn_Index: 2) -> arriving before Conn 1 is fully registered/acknowledged.
3. `DISCONNECT` (Triggered internally by Broker for Conn 1)
4. `CONNACK` (Sent to Conn 2)

**The Timing Hazard:** If Conn 2 arrives exactly in the window where Conn 1 is authenticating but not yet fully bound to the internal broker socket dictionary, async brokers can experience null pointer exceptions or enter an infinite loop of dropping both connections.

**TRE Fuzzing Value:** Model two independent timelines of event streams targeting the broker, constraining the time gap between overlapping `CONNECT` packets.

---

## 4. QoS 1/2 Message Flight Window Deflection
* **Target:** General MQTT Brokers (`amqtt`, `mosquitto`)
* **Concept:** When dealing with QoS 1 or QoS 2, brokers maintain an in-flight message queue. If a client goes offline and comes back online while messages are in flight, a sequence-timing bug often emerges.

### Discrete Event Sequence & Timing
1. Broker sends `PUBLISH` (QoS 2, MsgID: 1) to Client.
2. Client socket disconnects abruptly.
3. Client reconnects (`CONNECT` with `CleanSession=False`).
4. Client belatedly sends `PUBREC` for MsgID 1.

**The Timing Hazard:** Depending on whether the broker processes the new `CONNECT` event before or after it cleans up the dead socket's pending tasks, the `PUBREC` packet might arrive on a dead session context, leaving the message frozen in memory.

**TRE Fuzzing Value:** Involves discrete packets interleaved with network-level events (`link_down`, `link_up`), bound by specific timing constraints (e.g., "Disconnect happens within 5ms of a QoS2 Publish").

---

## Suggested TRE Formulation Strategy

To frame this for the uniform sampler, represent the alphabet Σ of the input signal as:

`Σ = { CONNECT, PUBLISH, DISCONNECT, PINGREQ, CONN_DROP }`

Express fuzzing constraints using standard TRE notation. For example, for Bug #1:

`CONNECT · T_1 · DISCONNECT · T_2 · CONN_DROP`

Where you explicitly force `T_2 ∈ [0, 2ms]` to sample the extreme edges of the thread lifecycle window. 
