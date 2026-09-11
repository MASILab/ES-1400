# ES-1400

Lab code for **ES 1401-11: Intro to Engineering Module** (Vanderbilt, MASI Lab). This repo holds the four hands-on lab projects for the course; everything else on the course schedule (agents, pulse coding, radio, keys/secrets, theremin, etc.) is lecture-only and has no code here.

Each lab runs on a Raspberry Pi unless noted otherwise, and uses `RPi.GPIO` for hardware control.

## Labs

### Lab-1 — Reinforcement Learning Tic-Tac-Toe

A progression of Tic-Tac-Toe implementations, each building on the last:

| File | Description |
|---|---|
| `TTT.py` | Basic two-player Tic-Tac-Toe (Tkinter GUI) |
| `TTT_RG.py` | Single player vs. a random-move computer opponent |
| `TTT_Min-Max.py` | Single player vs. a minimax (optimal) computer opponent |
| `TTT_RL.py` | Single player vs. a computer opponent trained with Q-learning (self-play); the trained Q-table is cached to `q_table.pkl` |

**Run:** `python3 TTT_RL.py` (or any of the other variants). Requires Tkinter (usually bundled with Python). No GPIO/hardware needed — this one runs fine on a laptop.

### Lab-2 — Candy Safe (magnetic card swipe + servo lock)

Simulates a card-locked candy safe: swipe a magnetic card to identify yourself, set a password, then swipe and enter the password again to unlock a servo-controlled latch.

| File | Description |
|---|---|
| `Swipe_Read.py` | Standalone helper to test reading raw magnetic card swipe data and extracting a student ID |
| `Lab2.py` | Full lab: swipe → extract ID → set password → re-swipe + re-enter password to verify → drive servo to the unlocked position |

**Run:** `python3 Lab2.py` on a Raspberry Pi with a USB magnetic card reader attached and a servo on GPIO pin 17 (BCM numbering).

### Lab-3 — Ultrasonic Sensing (theremin-style buzzer)

Reads distance from an HC-SR04 ultrasonic sensor and maps it to a buzzer tone in real time — closer objects produce a higher pitch (2–400 cm mapped to 200–2000 Hz).

**Run:** `python3 Lab3.py` on a Raspberry Pi with the ultrasonic sensor's trigger/echo pins on physical pins 7/11 (BOARD numbering) and a buzzer on pin 18. Ctrl-C to stop.

### Lab-4 — Networked Sensing

Extends Lab-3 across two Raspberry Pis: one measures distance and streams it over a TCP socket, the other receives the readings and plays the corresponding tone on its own buzzer.

| File | Description |
|---|---|
| `Lab4sender.py` | Runs on the "sensor" Pi — measures distance via the ultrasonic sensor and sends each reading to the receiver over a socket |
| `Lab4receiver.py` | Runs on the "buzzer" Pi — receives distance readings and converts them to a buzzer frequency |
| `send.py` / `receive.py` | Minimal standalone TCP messaging scripts, useful for testing connectivity between two Pis before running the full lab |

**Run:** on the receiver Pi, `python3 Lab4receiver.py` and enter a port to listen on; on the sender Pi, `python3 Lab4sender.py` and enter the receiver's IP address and the same port. Both Pis need to be on the same network.

## Requirements

- Python 3
- `RPi.GPIO` (Labs 2–4; Raspberry Pi only)
- Tkinter (Lab 1)
- Standard library only otherwise (`socket`, `termios`, `tty`, `getpass`, `pickle`, `random`)

## Repo layout

```
Lab-1/   Reinforcement learning Tic-Tac-Toe
Lab-2/   Candy Safe (card swipe + servo)
Lab-3/   Ultrasonic sensing (single Pi)
Lab-4/   Ultrasonic sensing over a network (two Pis)
```
