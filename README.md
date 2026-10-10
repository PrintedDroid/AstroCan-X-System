# AstroCan X -- The All-in-One Control System for Astromech Droids

<!-- webflash-notice -->
> **Notice:** AstroCan X firmware is released as ready-to-flash web installer in the [Printed Droid Firmware Flasher](https://www.printed-droid.com/firmware-flasher/). This repository holds the user handbooks; the documentation (commands, usage, settings) continues to be updated here and in the wiki.
>
> **Why:** Printed Droid has shared its source code openly for years. In the meantime, more and more projects in the community build on openly shared work but release their own results as closed source only. Open source works in both directions – this one-way street is not something we will keep supplying.

One system for everything in your droid: drive, dome, sound, lights, logic
displays, dozens of servos, panels and sensors -- all through one modern,
browser-based web interface, its own long-range radio link and a modular CAN +
wireless board ecosystem. No more patchwork of ten separate solutions -- one
coherent platform that grows with your droid.

> **Status:** technically mature, in its final polishing phase toward beta --
> stable enough for a full convention day, extensible enough for your own
> additions.

---

## What is in this repository

This repository is **documentation only** -- it does not contain firmware or
source code. It hosts the user handbooks so builders can read them before and
during a build. Firmware comes from the
[Firmware Flasher](https://www.printed-droid.com/firmware-flasher/).

AstroCan X has two web interfaces side by side -- the **Classic** view and the
newly structured **Next** view -- and there is a complete handbook for each:

| File | What it is |
|------|------------|
| `AstroCan_X_System_Documentation ...-classic.pdf` | **Handbook, Classic interface (English)** -- about 820 pages |
| `AstroCan_X_System_Documentation ...-classic_DE.pdf` | **Handbook, Classic interface (German)** -- about 850 pages |
| `AstroCan_X_System_Documentation ...-next.pdf` | **Handbook, Next interface (English)** -- about 690 pages |
| `AstroCan_X_System_Documentation ...-next_DE.pdf` | **Handbook, Next interface (German)** -- about 720 pages |
| `README.md` | This overview |

Both handbooks cover operation, concepts and step-by-step how-tos and are fully
illustrated with screenshots of the real web interface. Pick the one that
matches the interface you use. A separate Developer Reference (pinouts,
protocols, register maps) exists for firmware work and is not part of this
docs-only release.

---

## Introduction

Imagine a single system that controls everything in your droid -- drive, dome,
sound, lights, logic displays, dozens of servos, panels and sensors -- all
through one modern, browser-based web interface, its own long-range radio link
and a modular CAN and wireless board ecosystem.

AstroCan X is exactly that. It grew out of the original AstroCAN modules for
ShadowMD droids into a fully integrated system with its own remote. Behind it
are well over a year of development: countless iterations, a feature set that
spans from "plug-and-play for beginners" to "fully configurable for the pro
builder", and extensive, illustrated handbooks.

The system is modular and extensible. You start with the Core (radio + master)
and expand piece by piece -- every add-on board registers itself, shows up in the
interface and is ready to use immediately. No recompiling, no code-tinkering:
plug in the hardware, pick it in the web UI, done.

---

## System at a glance

```
  Remote(s) / RC / Handheld / App
        |
        |  long-range 2.4 GHz radio (frequency hopping, fixed, LoRa)  or  WiFi
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
- OLED display shows live droid status: battery, link quality, mode, now
  playing -- and why the droid is not driving right now (emergency stop,
  sensor hold, sticks back to neutral)
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
  own OLED + nav stick) that transmits over the long-range link, not WiFi -- so
  full drive control and range
- Voice control: wake word + commands on the Vision board
- Phone/tablet via the Touch-Remote, plus app, button board and the web UI
- Two remotes on one droid at the same time (driver + feature operator), cleanly
  separated in Two-Operator mode

### Its own long-range radio link

- Custom 2.4 GHz radio with frequency hopping across 80 channels in fixed time
  slots -- robust, interference-resistant, long range, even with hundreds of
  phones and WiFi networks around
- LoRa mode for maximum range at the press of a button
- Live telemetry back to the remote (battery, link quality, droid state);
  radio modes (frequency hopping / fixed / LoRa) switchable any time

### AstroCan X Core -- the heart on a single board

- Radio gateway and master controller on one PCB
- Everything on board: OLED display, audio output, CAN connection, SD slot and
  radio receiver

### CAN-Hub -- the robust backbone

- All body and dome modules on one automotive-grade CAN bus
- Central CAN-Hub with multiple connectors: plug in instead of star-wiring
- Plug-and-play while building and repairing: plug in or swap a board and it
  registers itself on the bus (type, firmware, capabilities); its functions
  appear automatically in the interface -- no recompiling, no protocol setup
- Cable first, radio as fallback: boards on the bus can also be paired by
  radio; as long as the cable is healthy it has priority, if it fails radio
  takes over
- Live status and auto-rejoin: real-time online/offline per board; wireless
  modules are paired once and rejoin by themselves afterwards
- Separate body and dome strands on one shared bus

### Drive and dome

- Eight motor driver types in one firmware (BLDC-PWM, Sabertooth, Cytron,
  RoboClaw, VESC (PPM or CAN), ODrive CAN, Roboteq CAN) -- switch via config, no
  recompiling
- Diamond mixing, smooth ramping, three drive modes (Slow/Normal/Turbo)
- AutoDome: full dome rotation with PID control and precise position control over
  CAN
- Dome Target-Lock (dual-gyro): keeps the head pointed at a fixed point in space
  no matter how the body drives or turns

### Familiar from day one -- MarcDuino and ShadowMD compatibility

- AstroCan X still speaks the classic MarcDuino / ShadowMD commands -- your
  familiar commands and existing panel sequences keep working
- The familiar command set runs alongside the modern one, so you migrate at your
  own pace
- Standalone firmwares for many boards run without a Core and understand the
  classic serial commands -- e.g. the Teeces logics with the original JawaLite
  command set

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

### AstroCan X Studio -- the workshop on your PC

- Windows application that connects to the droid over the network
- Track-based sequence editor (panels, servos, lift, lights, sound, logics) with
  curves, zoom, undo/redo and an explicitly armed preview
- Audio workshop: the complete SD sound library, waveform, tempo and beat
  detection
- Project files you can back up, share and compare with the droid field by
  field; encrypted backup of the droid's data
- Commissioning, fleet check against the firmware catalog and a workshop
  diagnostic run in which every board reports its bus and radio errors

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
- Sensor hold is self-clearing: the feet stop in front of an obstacle and drive
  again once the path is clear
- Patrol and wander modes: drive around autonomously, avoid obstacles, follow
  walls, back out of dead ends
- Vision board: camera with person and gesture detection
- Person-following: vision + sensors + drive together

### Multi-droid interaction

- Buddy mode: two droids paired over radio, with mirrored scenes and coordinated
  reactions

### Lights and displays -- over 80 animations

- BodyLights with multiple module groups (DPL, CBI, CSL, LDPL, UAL, VU and more),
  80+ animations, scene library, brightness profiles, one shared colour command
  for the whole fleet
- Logic displays and PSI, classic (Teeces) or fully digital (AstroCan DLL)
- Magic Panel, Periscope, Vent Logics, Tactical Display (round display with GIFs
  and tactical screens) and the round Radar Eye display
- Wireless light/display modules via the BridgeX board, paired straight from the
  web UI

### Audio

- Hi-fi audio from SD card, sound categories (chat/happy/scream/music),
  multi-track mixer (background loop + effect in parallel), overlays with smooth
  fade, loudness normalisation, droid speech

### Operation -- one web UI for everything

- Two web interfaces side by side: the Classic view and the modern Next view
  (German and English, dark/light themes, mobile-friendly)
- Dedicated pages for control, sequences, lights, servos, configuration and
  diagnostics
- Trigger-Pages for your phone: freely configurable button layouts, each tile
  bindable to a sequence/show/sound/scene, shared across devices
- Touch-Remote, setup wizard for first start, live health dashboard, command
  palette (Cmd+K), notifications

### Firmware, backup and maintenance

- Firmware Flasher in the browser: pick the board, plug in over USB, flash --
  every published version stays selectable, settings are kept unless you choose
  to erase
- OTA updates for the Core from the web UI; boards move step by step to a
  two-slot layout (new firmware is verified before it is activated, the old one
  stays as fallback) -- the basis for updates over the bus
- Complete backup and restore: settings survive a firmware reflash
- Export and import sequences, shows and profiles

### Deep diagnostics

- Live health dashboard, crash reports, per-board CAN heartbeat, board logs and
  telemetry logging to SD
- Every board on the bus reports its own error counters, boot and driver state
  on request -- for a diagnostic run without plugging USB into each board

### Safety first

- Emergency stop that latches and, from the factory, stops everything that moves
  (feet, dome, lift; servos hold, shows abort) -- nothing moves back on its own.
  Which areas it stops is configurable (feet always). The latch survives a
  restart; release deliberately in the web interface or on the remote by holding
  the E-Stop button for 3 seconds with the sticks at neutral
- Radio-loss failsafe (hold, ramp, stop), multi-layer runaway protection
- Under-voltage cutoff, watchdogs, drive heartbeat, valet/transport lockout
  (motors hard-disabled), child lock
- Foot motors can only be driven from the remote -- never from phone, web UI,
  app or automation
- Two-Operator mode and Instructor mode (teacher override for beginners)

### Smart home and automation

- MQTT with Home Assistant auto-discovery, REST API, webhooks (in and out)
- Schedule mode with NTP; WiFi as an access point and on your home network at the
  same time

### Convention-ready

- Convention mode with large tap buttons, usage statistics, one-tap mood presets,
  saveable droid profiles

### Grows with you -- the board ecosystem

More than 30 boards and form factors on the CAN bus or wireless, each with its
own firmware in the Firmware Flasher -- plus around 20 standalone firmwares for
droids without a Core:
ServoBoard, AutoDome, Sense, Vision, DomeLift, CSL+, CSL, UAL, D-DPL / RGB-DPL
BodyLights, AstroCan DLL, Teeces (C3 and S3), Magic Panel and Magic Panel HD,
Periscope, Vent Logics, Tactical Display, Radar Eye, Dome Button Controller,
Buttonboard, Config Display, BridgeX, Feature X, Mini-Remote, Lightsaber-Remote
and more.

---

## Documentation

- **User handbooks (this repo):** one for the Classic interface and one for the
  Next interface, each in English and German, roughly 700 to 850 pages each,
  illustrated with real web-interface screenshots, with step-by-step guides.
- A separate **Developer Reference** covers pinouts, protocols, byte layouts, NVS
  keys and register maps (not part of this docs-only release).

Start with the handbook for your interface in your language. It walks you from
the first boot and setup wizard through everyday operation to the advanced
sequence, lighting and automation features.

---

## Project status and license

AstroCan X is in its final polishing phase toward a public beta. The firmware and
the interface are feature-complete for real convention use; work now focuses on
stabilisation and documentation.

This project and its documentation are intended for personal use and for
Astromech community members. Star Wars, R2-D2 and related names are trademarks of
their respective owners.
