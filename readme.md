# MicroPython Driver for Waveshare 2.9" e‑Paper B V3 (Black/White/Red)

A fast, feature‑rich MicroPython driver for the **Waveshare 2.9inch e‑Paper B V3** display (128×296 pixels, black/white/red).  
Optimised for ESP32‑S3 Zero, but works on any MicroPython board with SPI.


## Features

- Full black, white and red support

- Rotation (0°, 90°, 180°, 270°)

- Drawing primitives: pixels, lines, rectangles (filled/outline), circles, triangles

- Text rendering with built‑in 5×7 pixel font (ASCII 32–122)

- Automatic scaling, centering, and “fit to width” for text

- Low‑power sleep mode

- Simple 6‑pin SPI connection

## Wiring

| Display Pin | ESP32‑S3 Zero | GPIO |
| - | - | - |
| BUSY | GPIO11 | 11 |
| RST | GPIO5 | 5 |
| D/C | GPIO12 | 12 |
| CS | GPIO13 | 13 |
| CLK | GPIO4 | 4 |
| MOSI | GPIO3 | 3 |
| (MISO) | not connected | – |


> **Note:** MISO is not used by the display – you can leave it unconnected.

## Installation

1. Copy `epaper2in9bv3.py` to your MicroPython device (e.g. `/lib/epaper2in9bv3.py`).

2. Use the following example to test the display.

## Basic Usage

```
from epaper2in9bv3 import EPaper29BV3      
      
\\\\\\\# Initialise with default pins (or override with custom pins)      
ep = EPaper29BV3()      
      
\\\\\\\# Must call init() once after power‑up      
ep.init()      
ep.clear()      
      
\\\\\\\# Draw black text, red rectangle      
ep.text(ep.BK, "Hello World!", 10, 20, scale=2)      
ep.fill\\\\\\\_rect(ep.RD, 10, 50, 100, 30)      
      
\\\\\\\# Send to display      
ep.show()      
      
\\\\\\\# Put display to sleep when done      
ep.sleep()
```

