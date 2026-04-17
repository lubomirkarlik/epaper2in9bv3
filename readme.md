# MicroPython Driver for Waveshare 2.9" e-Paper B V3 (Black/White/Red)

A fast, feature-rich MicroPython driver for the **Waveshare 2.9inch e-Paper B V3** display (128×296 pixels, black/white/red).  
Optimised for ESP32-S3 Zero, but works on any MicroPython board with SPI.

![2.9"eInk dispolay](img/ePap29.png)

## Features

- Full black, white and red support
- Rotation (0°, 90°, 180°, 270°)
- Drawing primitives: pixels, lines, rectangles, circles, triangles
- Text rendering with built-in 5×7 font (ASCII 32–122)
- Automatic scaling, centering, and “fit to width” text
- Low-power sleep mode
- Simple 6-pin SPI connection

## Wiring

| **Display Pin** | **ESP32-S3 Zero** | **GPIO** |
| :-: | :-: | :-: |
| BUSY | GPIO11 | 11 |
| RST | GPIO5 | 5 |
| D/C | GPIO12 | 12 |
| CS | GPIO13 | 13 |
| CLK | GPIO4 | 4 |
| MOSI | GPIO3 | 3 |
| (MISO) | not connected | – |


> **Note:** MISO is not used by the display.

## Installation

Copy `epaper2in9bv3.py` to your device:

```
/lib/epaper2in9bv3.py
```

## Basic Usage

```
from epaper2in9bv3 import EPaper29BV3  
ep = EPaper29BV3()  
ep.init()  
ep.clear()  
ep.text(ep.BK, "Hello World!", 10, 20, scale=2)  
ep.fill_rect(ep.RD, 10, 50, 100, 30)  
ep.show()  
ep.sleep()
```

## Example: Drawing

```
ep.clear()  
ep.circle(ep.BK, 64, 80, 30)  
ep.fill_rect(ep.RD, 20, 140, 80, 40)  
ep.text_center(ep.BK, "Demo", 10, scale=2)  
ep.show()
```

## Rotation

```
ep = EPaper29BV3(rotation=90)
```
- Supported: `0, 90, 180, 270`
- Width and height adjust automatically
> Rotation is handled in software.

## Custom Pins

```
ep = EPaper29BV3(cs=5,dc=17,rst=16,busy=4,clk=18,mosi=23)
```

## Memory Usage

- Resolution: 128 × 296 pixels
- Framebuffer per channel: 4736 bytes
- Total RAM usage: ~9.5 KB

## Important Notes

- Full refresh takes ~2–3 seconds (normal for ePaper)
- Always call `sleep()` before cutting power
- No partial refresh support (full refresh only)
- Framebuffer uses inverted logic:
  - `0 = pixel ON (black/red)`
  - `1 = pixel OFF (white)`

## Compatibility

Tested on:

- ESP32-S3 Zero

Should work on:
- ESP32
- RP2040 (Raspberry Pi Pico)
- ESP8266 (limited RAM)

## Documentation

Full API specification available in SPEC.md

## License

MIT – free for personal and commercial use.

