# Firmware

Built with PlatformIO; configuration is `../platformio.ini`.

| Folder              | Contents                                                        |
| ------------------- | --------------------------------------------------------------- |
| `arduino-original/` | The sketch as written in the Arduino IDE. Reference only, not built. |
| `src/`              | Converted sources. `main.cpp` holds `setup()` and `loop()`.     |
| `include/`          | Headers, e.g. `pins.h` (fan pin map), `notes.h` (sequence and timing). |
| `lib/`              | Private libraries, one folder each (`lib/<Name>/src/...`).      |
| `test/`             | Unit tests run with `pio test`.                                 |

## Converting the `.ino` to C++

The Arduino IDE quietly preprocesses sketches. PlatformIO compiles plain C++,
so those steps become explicit:

1. Copy the sketch into `arduino-original/<sketch_name>/<sketch_name>.ino`
   (the Arduino IDE requires the folder and file names to match).
2. Copy its contents into `src/main.cpp`.
3. Add `#include <Arduino.h>` as the first line.
4. Declare every function above its first use (the IDE generated these
   prototypes automatically), or move the definitions above `setup()`.
5. If the sketch had several tabs (extra `.ino` files), the IDE concatenated
   them. Split them into `.cpp` files in `src/` with matching headers in
   `include/`.
6. Libraries installed through the Arduino Library Manager go in
   `lib_deps` in `platformio.ini`, not in a global install.
7. Build with `pio run`, upload with `pio run -t upload`.
