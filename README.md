# four-tone

An Arduino plays a sequence of four notes by switching four 12 V 5015 blower
fans. Each fan blows into a 3D printed, recorder-style beak fitted with a 2" PVC
pipe, so each fan/pipe pair sounds one note. See `hardware/parts.md` for the
parts list.

## Layout

```
four-tone/
├── platformio.ini            PlatformIO build config (CLion opens the repo root)
├── firmware/                 Arduino code
│   ├── arduino-original/     The original .ino sketch, kept for reference
│   ├── src/                  Converted C++ sources (main.cpp)
│   ├── include/              Project headers (pin map, note sequence, config)
│   ├── lib/                  Project-private libraries
│   └── test/                 PlatformIO unit tests
├── hardware/
│   ├── pcb/                  KiCad project for the Arduino carrier / fan driver board
│   │   ├── libraries/        Project-specific symbols, footprints, 3D models
│   │   └── fabrication/      Released Gerbers, drill, BOM, placement, one folder per revision
│   └── datasheets/           Fans, MOSFETs, connectors, regulators
├── mechanical/
│   ├── cad/                  FreeCAD models: beak and fan caddy
│   ├── stl/                  Print-ready exports
│   ├── slicer/               Slicer projects (.3mf); sliced G-code is not committed
│   └── enclosure/            Open-bottom wooden box for the voices and power supply
└── docs/                     Build notes, wiring, tuning, photos
```

## Firmware in CLion

1. Install PlatformIO Core: `brew install platformio` (or `pipx install platformio`).
2. In CLion, install the **PlatformIO for CLion** plugin.
3. Open the repo root. CLion detects `platformio.ini` and offers the PlatformIO
   run configurations (Build, Upload, Monitor).

See `firmware/README.md` for converting the `.ino` sketch.

## License

Copyleft throughout: firmware under GPL-3.0-or-later, hardware under
CERN-OHL-S-2.0, and mechanical design and documentation under CC-BY-SA-4.0.
See [LICENSE.md](LICENSE.md) for details.
