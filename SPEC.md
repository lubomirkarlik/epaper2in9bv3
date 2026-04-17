# **Software Specification – Waveshare 2.9" e-Paper B V3 Driver**

**Driver version:** 1.0  
**Target platform:** MicroPython (tested on ESP32-S3 Zero)  
**Display:** 2.9 inch, 128×296 pixels, black/white/red, SPI interface


## API Overview

| Method | Description |
| - | - |
| init() | Initialise the display (call once) |
| show() | Transfer both framebuffers and refresh |
| sleep() | Deep sleep mode |
| clear() | Clear both framebuffers to white |
| fill(color) | Fill entire display with WHITE / BLACK / RED |
| pixel(ch, x, y) | Set a single pixel in BK or RD channel |
| pixel\_off(ch, x, y) | Clear a single pixel (set to white) |
| hline(ch, x, y, len) / vline(...) | Horizontal / vertical line |
| line(ch, x0,y0, x1,y1) | Line between two points |
| draw\_rect(ch, x, y, w, h) | Rectangle outline |
| fill\_rect(ch, x, y, w, h) | Filled rectangle |
| clear\_rect(ch, x, y, w, h) | Clear rectangle to white |
| circle(ch, x0, y0, r, filled) | Circle or disk |
| triangle(ch, x0,y0, x1,y1, x2,y2, filled) | Triangle |
| text(ch, txt, x, y, scale=1) | Render text |
| text\_center(ch, txt, y, scale=1) | Centered horizontally |
| text\_fit(ch, txt, y, max\_scale=3) | Automatically choose largest scale |
| text\_width(txt, scale) | Width of text in pixels |


## Colour Constants

- `EPaper29BV3.WHITE = 0`

- `EPaper29BV3.BLACK = 1`

- `EPaper29BV3.RED = 2`

**Channel selection:**

- `EPaper29BV3.BK = 0` (black channel)

- `EPaper29BV3.RD = 1` (red channel)


## Rotation

Set during construction:

```
`ep = EPaper29BV3(rotation=90)`
```

- Supported: `0, 90, 180, 270`

- Logical `width` and `height` are automatically swapped for 90° and 270°

**Note:**  
Rotation is applied in software. Internal framebuffer orientation is fixed and does not match logical coordinates directly.


## 1. Class: EPaper29BV3

### Constructor

```
`EPaper29BV3(cs=13, dc=12, rst=5, busy=11, clk=4, mosi=3, miso=16, rotation=0)`
```

| Parameter | Type | Default | Description |
| - | - | - | - |
| cs | int | 13 | Chip Select pin |
| dc | int | 12 | Data/Command pin |
| rst | int | 5 | Reset pin |
| busy | int | 11 | Busy pin |
| clk | int | 4 | SPI clock |
| mosi | int | 3 | SPI MOSI |
| miso | int | 16 | SPI MISO (unused) |
| rotation | int | 0 | Display rotation |

### Properties

- `width` – logical width after rotation (read-only)

- `height` – logical height after rotation (read-only)


## 2. Initialisation & Power Management

### init() -\> None

Initialises the display controller.  
Must be called once after power-on.


### show() -\> None

Transfers both framebuffers and triggers a full refresh.

- Blocking operation (≈2–3 seconds)

- Waits until BUSY pin goes low

**Note:**  
If the display does not respond, the internal wait may timeout, but no exception is raised.


### sleep() -\> None

Puts display into deep sleep.

- Required before cutting power

- Device will not respond until reset or power cycle


### clear() -\> None

Clears both framebuffers (sets all pixels to white).  
Does not update display — call `show()` afterwards.


### fill(color: int) -\> None

Fills display with a single colour.

| Color | Effect |
| - | - |
| WHITE | Clears both channels |
| BLACK | Sets black channel only |
| RED | Sets red channel only |


## 3. Framebuffer & Pixel Model

- Each channel has its own framebuffer

- Size per channel: `128 × 296 / 8 = 4736 bytes`

- Bit format:

  - `0 = pixel ON (black/red)`

  - `1 = pixel OFF (white)`


## 4. Pixel Operations

### pixel(channel, x, y)

Sets a pixel (black or red depending on channel).

- Applies rotation automatically

- Out-of-bounds coordinates are ignored


### pixel\_off(channel, x, y)

Clears pixel (sets to white).


## 5. Drawing Primitives

All coordinates are logical (after rotation).

### hline / vline

Draw horizontal or vertical line.


### line

Draw line using Bresenham’s algorithm.


### draw\_rect

Draw rectangle outline.


### fill\_rect

Draw filled rectangle.


### clear\_rect

Clear rectangle to white.


### circle

Draw circle or filled disk.


### triangle

Draw triangle (outline or filled).


## 6. Text Rendering

- Built-in 5×7 pixel font

- ASCII range: 32–122

- Unsupported characters rendered as space


### char(channel, x, y, ch, scale=1) -\> int

Draw a single character.

Returns next X position.


### text(channel, txt, x, y, scale=1)

Draw string.


### text\_width(txt, scale=1) -\> int

Returns pixel width:

```
`len(txt) \* (5 \* scale + scale) - scale`
```


### text\_center(channel, txt, y, scale=1)

Draw centered text.


### text\_fit(channel, txt, y, max\_scale=3) -\> int

Finds largest scale that fits screen width.

- Uses margin of 8 pixels

- Returns used scale


## 7. Internal Methods (private)

| Method | Description |
| - | - |
| \_cmd(c) | Send command |
| \_data(d) | Send data |
| \_wait(timeout) | Wait for BUSY pin |
| \_reset() | Hardware reset |
| \_buf(channel) | Get framebuffer |
| \_get\_char(ch) | Font lookup |


## 8. Constants

| Name | Value | Meaning |
| - | - | - |
| WHITE | 0 | White |
| BLACK | 1 | Black |
| RED | 2 | Red |
| BK | 0 | Black channel |
| RD | 1 | Red channel |
| W | 128 | Physical width |
| H | 296 | Physical height |


## 9. Timing & Dependencies

- SPI speed: 2 MHz

- Refresh time: ~2–3 seconds

- BUSY pin: `1 = busy`, `0 = idle`

- Uses:

  - `machine.Pin`

  - `machine.SoftSPI`

  - `time`


## 10. Notes

- Display refresh is slow (normal for ePaper)

- Always call `sleep()` before power-off

- No partial refresh support


## 11. Example

```
`from epaper2in9bv3 import EPaper29BV3`

`import time`


`ep = EPaper29BV3(rotation=0)`

`ep.init()`

`ep.clear()`


`ep.circle(ep.BK, 64, 100, 40)`

`ep.fill\_rect(ep.RD, 20, 160, 88, 40)`


`ep.text\_fit(ep.BK, "Hello ePaper", 240)`

`ep.show()`


`time.sleep(5)`

`ep.sleep()`
```


## 12. Revision History

| Version | Date | Changes |
| - | - | - |
| 1.0 | 2026-04-12 | Initial release |
| 1.1 | 2026-04-17 | Specification aligned with implementation |


