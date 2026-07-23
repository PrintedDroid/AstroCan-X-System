# AstroCan X -- The All-in-One Control System for Astromech Droids

One system for everything in your droid: drive, dome, sound, lights, logic
displays, dozens of servos, panels and sensors -- all through one modern,
browser-based web interface, its own long-range radio link and a modular CAN +
wireless board ecosystem. No more patchwork of ten separate solutions -- one
coherent platform that grows with your droid.

> **Status:** technically mature, in its final polishing phase toward beta --
> stable enough for a full convention day, extensible enough for your own
> additions. Handbook build v3.11.114 (2026).

---

## What is in this repository

This repository is **documentation only** -- it does not contain firmware or
source code. It exists to host the user handbook so builders can read it before
and during a build.

| File | What it is |
|------|------------|
| `AstroCan_X_System_Documentation.pdf` | **User handbook (English)** -- operation, concepts, step-by-step how-tos, illustrated |
| `AstroCan_X_System_Documentation_DE.pdf` | **User handbook (German)** -- same content, in German |
| `README.md` | This overview |

The handbook is over **770 pages** per language and is fully illustrated with
screenshots of the real web interface. A separate Developer Reference (pinouts,
protocols, register maps) exists for firmware work and is not part of this
docs-only release.

---

## Introduction

Imagine a single system that controls everything in your droid -- drive, dome,
sound, lights, logic displays, dozens of servos, panels and sensors -- all
through one modern, browser-based web interface, its own long-range radio link
and a modular CAN and wireless board ecosystem.

AstroCan X is exactly that. Behind the project are over a year of development and
hundreds of hours of work: countless iterations, a feature set that spans from
"plug-and-play for beginners" to "fully configurable for the pro builder", and
an extensive, illustrated handbook.

The system is modular and extensible. You start with the Core (radio + master)
and expand piece by piece -- every add-on board registers itself, shows up in the
interface and is ready to use immediately. No recompiling, no code-tinkering:
plug in the hardware, pick it in the web UI, done.

---

## System at a glance

```
  Remote(s) / RC / Handheld / App
        |
        |  long-range 2.4 GHz radio (FLRC/FHSS, LoRa, ESP-NOW)  or  WiFi
        v
  AstroCan X Core  =  Gateway (radio + WiFi + web UI)  --on-board UART-->  Master
                                                                    (motor/audio/CAN)
        |                                                               |
        |  WiFi: web UI, app, REST/MQTT                                 |  CAN bus + wireless
        v                                                               v
  Browser / Phone / Home Assistant                        Body + Dome module ecosystem
                                                          (ServoBoard, AutoDome, Sense,
                                                           Vision, BodyLights, logic
                                                           displays, Magic Panel, ...)
```

---

## Feature highlights

### The AstroCan X Mini-Remote -- tiny, but it has it all

- Compact one-hand form factor: every key function reachable with your thumb --
  built for a full convention day
- 2 joysticks = 4 control channels at 11-bit precision (2048 steps per axis) --
  eight times finer than standard RC, for smooth driving and dome fine-tuning
- Over 20 freely assignable buttons: 16 top buttons, 5 side buttons and a
  navigation stick
- Each button can do four actions: short / long / double / chord (two buttons
  together) -- turning a tiny remote into dozens of functions
- Gyro gestures as extra inputs (tilting/moving triggers actions)
- OLED display shows live droid status: battery, link quality, mode, now playing
- Up to 4 droid profiles, switchable on the fly
- Its own long-range radio, battery-powered with deep sleep

### The Lightsaber-Remote -- a full remote inside a prop

- A complete remote control hidden inside a lightsaber -- and just as easily
  built into any other prop (staff, blaster, belt gadget)
- Control through motion: gyro gestures recognise lifting, dropping and twirling
- Configurable buttons (3-6) + optional OLED, its own long-range radio, deep
  sleep for long prop runtime
- 3 banks (Combat / Performance / Background) with nameable assignments
- The control stays completely invisible to the audience

### Control it any way you like

- Classic RC transmitters via SBUS/iBUS -- up to 2 receivers at once, even in
  mixed mode (an SBUS receiver and an iBUS receiver side by side, each on its own
  port). Freely configurable from 4 to 16 channels per input
- ExpressLRS (ELRS) fully supported
- Steam Deck, Windows handhelds and gamepads via a compact USB dongle (with its
  own OLED + nav stick) that transmits over ELRS -- the real long-range link, not
  WiFi, so full drive control and range
- Voice control: wake word + commands on the Vision board
- Phone/tablet via the Touch-Remote, plus app, button board and the web UI
- Up to two control sources in parallel (driver + feature operator), cleanly
  separated in Two-Operator mode

### Its own long-range radio link

- Custom 2.4 GHz radio on the SX1280 (FLRC) with frequency hopping across 80
  channels -- robust, interference-resistant, long range
- LoRa fallback for maximum range at the press of a button
- Live telemetry back to the remote (battery, link quality, status); multiple
  radio modes (FHSS / Fixed / LoRa / ESP-NOW) switchable any time

### AstroCan X Core -- the heart on a single board

- Radio gateway and master controller on one PCB
- Everything on board: OLED display, I2S audio DAC, CAN transceiver, SD slot and
  radio receiver

### CAN-Hub -- the robust backbone

- All body and dome modules on one automotive-grade CAN bus
- Central CAN-Hub with multiple connectors: plug in instead of star-wiring
- Plug-and-play while building and repairing: plug in or swap a board and it
  registers itself on the bus (type, firmware, capabilities); its functions
  appear automatically in the interface -- no recompiling, no protocol setup
- Live status and auto-rejoin: real-time online/offline per board; wireless
  modules are paired once (encrypted) and rejoin by themselves afterwards
- Separate body and dome strands on one shared bus

### Drive and dome

- Multiple motor drivers in one firmware (Sabertooth, Cytron, RoboClaw, BLDC-PWM,
  VESC) -- switch via config, no recompiling
- Diamond mixing, smooth ramping, three drive modes (Slow/Normal/Turbo),
  emergency stop and failsafe included
- AutoDome: full dome rotation with PID control and precise position control over
  CAN
- Dome Target-Lock (dual-gyro): keeps the head pointed at a fixed point in space
  no matter how the body drives or turns

### Familiar from day one -- MarcDuino and ShadowMD compatibility

- AstroCan X still speaks the classic MarcDuino / ShadowMD commands -- your
  familiar commands and existing panel sequences keep working
- The familiar command set runs alongside the modern one, so you migrate at your
  own pace

### Sequence editor and show system

- Drag-and-drop lane editor in the browser: move, trim and reorder command
  blocks, with a full command palette
- 64 sequence slots, a show library with curated shows, copy-to-slot, undo, live
  validation
- Over 80 classic MarcDuino shows for R2-D2, Chopper and BT-1 as fully editable
  chains
- Music authoring: automatic BPM detection, beat markers, beat-synced waits and
  beat-synced light shows
- Live cue recording, audio FFT bands, frame/panel editor

### Servos without end

- ServoBoard with up to 32 servos per board, and several boards at once (well
  over 90 servo channels in a full build)
- Semantic control (open/close/mid/percent instead of raw microseconds), 8 easing
  curves per servo, named servo groups, sweep, reverse, calibration -- all from
  the web UI
- Door assignments link servos to light effects; MarcDuino panel sequences fully
  ported; Maestro compatibility for existing setups

### Sensors and autonomous driving

- Sense board for collision avoidance: ToF distance sensors around the skirt, in
  zones (front/side/rear) with configurable thresholds and reactions
- Live radar in the web UI: sensor angle, field-of-view cones and real-time
  distances, graphically
- Patrol and wander modes: drive around autonomously, avoid obstacles, follow
  walls, back out of dead ends
- Person-following: vision + sensors + drive together

### Multi-droid interaction

- Time-synced shows between two droids
- Automatic greeting on approach and call-and-response between droids

### Lights and displays -- over 80 animations

- BodyLights with multiple module groups (DPL, CBI, CSL, LDPL, UAL, VU and more),
  80+ animations, scene library, brightness profiles, one shared colour command
  for the whole fleet
- Logic displays and PSI, classic (Teeces v5) or fully digital (AstroCan DLL)
- Magic Panel, Periscope, Tactical Display (round display with GIFs and tactical
  screens)
- Wireless light/display modules via the BridgeX board over ESP-NOW, with
  encrypted pairing straight from the web UI

### Audio

- I2S hi-fi audio from SD card, sound categories (chat/happy/scream/music),
  multi-track mixer (background loop + effect in parallel), overlays with smooth
  fade, loudness normalisation

### Operation -- one web UI for everything

- Modern, mobile-friendly web interface (German and English, dark/light themes)
- Dedicated pages for control, sequences, lights, servos, configuration and
  diagnostics
- Trigger-Pages for your phone: freely configurable button layouts, each tile
  bindable to a sequence/show/sound/scene, shared across devices
- Touch-Remote, setup wizard for first start, live health dashboard, command
  palette (Cmd+K), notifications

### Backup, export and maintenance

- Complete backup and restore to the SD card: settings survive a firmware reflash
- Export and import sequences, shows and profiles
- OTA updates over WiFi -- flash new firmware from the web UI, no cable

### Deep diagnostics

- Live health dashboard, crash reports, per-board CAN heartbeat, board logs and
  telemetry logging to SD

### Safety first

- Global emergency stop, radio-loss failsafe (hold/centre/stop), multi-layer
  runaway protection
- Under-voltage cutoff, watchdog, valet/transport lockout (motors hard-disabled),
  child lock
- Two-Operator mode and Instructor mode (teacher override for beginners)

### Smart home and automation

- MQTT with Home Assistant auto-discovery, REST API, webhooks (in and out)
- Schedule mode with NTP; WiFi as an access point and on your home network at the
  same time

### Convention-ready

- Convention mode with large tap buttons, usage statistics, one-tap mood presets,
  saveable droid profiles

### Grows with you -- the board ecosystem

More than a dozen documented add-on boards on the CAN bus or wireless:
ServoBoard, AutoDome, Sense, Vision, Domelift, CSL+, D-DPL / RGB-DPL BodyLights,
AstroCan DLL, Teeces v5, Magic Panel, Periscope, Tactical Display, Dome Button
Controller, Buttonboard, BridgeX and more.

---

## Documentation

- **User handbook (this repo):** over 770 pages per language, English and German,
  illustrated with real web-interface screenshots, with step-by-step guides.
- A separate **Developer Reference** covers pinouts, protocols, byte layouts, NVS
  keys and register maps (not part of this docs-only release).

Start with the System Documentation PDF in your language. It walks you from the
first boot and setup wizard through everyday operation to the advanced sequence,
lighting and automation features.

---

## Project status and license

AstroCan X is in its final polishing phase toward a public beta. The firmware and
the interface are feature-complete for real convention use; work now focuses on
stabilisation and documentation.

This project and its documentation are intended for personal use and for
Astromech community members. Star Wars, R2-D2 and related names are trademarks of
their respective owners; this is a non-commercial fan project.
