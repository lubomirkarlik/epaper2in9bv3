## \***API Overview**

| \***Method** | \***Description** |
| :-: | :-: |
| \***`init()`** | \***Initialise the display (call once)** |
| \***`show()`** | \***Transfer both framebuffers and refresh** |
| \***`sleep()`** | \***Deep sleep mode** |
| \***`clear()`** | \***Clear both framebuffers to white** |
| \***`fill(color)`** | \***Fill entire display with WHITE / BLACK / RED** |
| \***`pixel(ch, x, y)`** | \***Set a single pixel in BK or RD channel** |
| \***`hline(ch, x, y, len)` / `vline(...)`** | \***Horizontal / vertical line** |
| \***`line(ch, x0,y0, x1,y1)`** | \***Line between two points** |
| \***`rect(ch, x, y, w, h)`** | \***Rectangle outline** |
| \***`fill\\\_rect(ch, x, y, w, h)`** | \***Filled rectangle** |
| \***`circle(ch, x0, y0, r, filled)`** | \***Circle or disk** |
| \***`triangle(ch, x0,y0, x1,y1, x2,y2, filled)`** | \***Triangle** |
| \***`text(ch, txt, x, y, scale=1)`** | \***Render text** |
| \***`text\\\_center(ch, txt, y, scale=1)`** | \***Centered horizontally** |
| \***`text\\\_fit(ch, txt, y, max\\\_scale=3)`** | \***Automatically choose largest scale that fits** |
| \***`text\\\_width(txt, scale)`** | \***Width of text in pixels** |


## \***Colour Constants**

- \***`EPaper29BV3.WHITE` = 0**

- \***`EPaper29BV3.BLACK` = 1**

- \***`EPaper29BV3.RED` = 2**

\***Channel select for drawing:**

- \***`EPaper29BV3.BK` = 0 (black channel)**

- \***`EPaper29BV3.RD` = 1 (red channel)**

## \***Rotation**

\***Pass `rotation=` when creating the object:**

**python**

```
\*\*\*ep = EPaper29BV3(rotation=90)   \\\# landscape, 128x296 becomes 296x128 logical\*\*
```

\***Logical width/height are swapped automatically for 90° and 270°.**

## \***Notes**

- \***The display is slow – a full refresh takes ~2‑3 seconds.**

- \***Always call `sleep()` before cutting power to prevent damage.**

- \***BUSY pin is `1` = busy, `0` = idle (handled automatically by the driver).**

## \***License**

\***MIT – use freely in personal and commercial projects.**

# Software Specification – Waveshare 2.9" e-Paper B V3 Driver

**Driver version:** 1.0  
**Target platform:** MicroPython (tested on ESP32‑S3 Zero)  
**Display:** 2.9 inch, 128×296 pixels, black/white/red, SPI interface

## 1. Class: `EPaper29BV3`

### 1.1 Constructor

```
EPaper29BV3(cs=13, dc=12, rst=5, busy=11, clk=4, mosi=3, miso=16, rotation=0)
```

| \***Parameter** | \***Type** | \***Default** | \***Description** |
| :-: | :-: | :-: | :-: |
| \***`cs`** | \***`int`** | \***13** | \***Chip Select pin number** |
| \***`dc`** | \***`int`** | \***12** | \***Data/Command pin number** |
| \***`rst`** | \***`int`** | \***5** | \***Reset pin number** |
| \***`busy`** | \***`int`** | \***11** | \***Busy status pin number** |
| \***`clk`** | \***`int`** | \***4** | \***SPI clock pin** |
| \***`mosi`** | \***`int`** | \***3** | \***SPI MOSI pin** |
| \***`miso`** | \***`int`** | \***16** | \***SPI MISO pin (not used, but required by SoftSPI)** |
| \***`rotation`** | \***`int`** | \***0** | \***Display rotation: 0, 90, 180, 270 degrees** |


\***Properties:**

- \***`width` – logical width after rotation (read‑only)**

- \***`height` – logical height after rotation (read‑only)**

## \***2. Initialisation & Power Management**

### \***`init() -\\\> None`**

\***Initialises the display controller. Must be called once after power‑on or after a hardware reset.**  
**Side effect: The display enters idle mode.**

### \***`sleep() -\\\> None`**

\***Sends the deep‑sleep command. After this, the display will not respond to commands until a hardware reset or power cycle.**  
**Must be called before cutting power to the display.**

### \***`show() -\\\> None`**

\***Transfers both framebuffers (black and red) to the display memory and triggers a full refresh.**  
**Blocks until the BUSY pin goes low (typically 2–3 seconds).**  
**Raises: `RuntimeError` if a timeout occurs (default 20 seconds).**

### \***`clear() -\\\> None`**

\***Clears both internal framebuffers to white (all bits = 1). Does not update the display – call `show()` afterwards.**

### \***`fill(color: int) -\\\> None`**

\***Fills the entire logical display area with a single colour.**

| \***`color`** | \***Effect** |
| :-: | :-: |
| \***`WHITE` (0)** | \***Clears both channels (white)** |
| \***`BLACK` (1)** | \***All pixels black** |
| \***`RED` (2)** | \***All pixels red** |


## \***3. Framebuffer Access (Pixel Operations)**

\***All drawing methods accept a channel parameter:**

- \***`BK` (0) – black channel**

- \***`RD` (1) – red channel**

### \***`pixel(channel: int, x: int, y: int) -\\\> None`**

\***Sets a pixel to black (on BK channel) or red (on RD channel).**  
**Applies the current rotation automatically. Coordinates outside the logical display are ignored.**

### \***`pixel\\\_off(channel: int, x: int, y: int) -\\\> None`**

\***Clears a pixel (sets it to white) on the specified channel.**

## \***4. Drawing Primitives**

\***All coordinates are logical (after rotation).**

### \***`hline(channel: int, x: int, y: int, length: int) -\\\> None`**

\***Draws a horizontal line of `length` pixels starting at `(x, y)`.**

### \***`vline(channel: int, x: int, y: int, length: int) -\\\> None`**

\***Draws a vertical line of `length` pixels starting at `(x, y)`.**

### \***`line(channel: int, x0: int, y0: int, x1: int, y1: int) -\\\> None`**

\***Draws a straight line between `(x0, y0)` and `(x1, y1)` using Bresenham’s algorithm.**

### \***`draw\\\_rect(channel: int, x: int, y: int, w: int, h: int) -\\\> None`**

\***Draws an unfilled rectangle (outline only). Top‑left corner `(x, y)`, width `w`, height `h`.**

### \***`fill\\\_rect(channel: int, x: int, y: int, w: int, h: int) -\\\> None`**

\***Draws a filled rectangle.**

### \***`clear\\\_rect(channel: int, x: int, y: int, w: int, h: int) -\\\> None`**

\***Clears a rectangle to white (sets pixels off).**

### \***`circle(channel: int, x0: int, y0: int, r: int, filled: bool = False) -\\\> None`**

\***Draws a circle (`filled=False`) or a filled disk (`filled=True`) centered at `(x0, y0)` with radius `r`.**

### \***`triangle(channel: int, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, filled: bool = False) -\\\> None`**

\***Draws a triangle. The three vertices are given as `(x0,y0)`, `(x1,y1)`, `(x2,y2)`. If `filled=True`, the triangle is filled using horizontal scanlines.**

## \***5. Text Rendering**

\***The driver includes a built‑in 5×7 pixel monospaced font covering ASCII 32–122.**  
**Unsupported characters are rendered as a space.**

### \***`char(channel: int, x: int, y: int, ch: str, scale: int = 1) -\\\> int`**

\***Renders a single character at `(x, y)` with an optional integer scale factor (1 = 5×7, 2 = 10×14, …).**  
**Returns the X coordinate after the character (useful for manual placement).**

### \***`text(channel: int, txt: str, x: int, y: int, scale: int = 1) -\\\> None`**

\***Renders a whole string. Characters are placed with one scale‑unit gap between them.**

### \***`text\\\_width(txt: str, scale: int = 1) -\\\> int`**

\***Returns the total pixel width of the string when rendered with the given scale.**  
**Formula: `len(txt) \\\* (5 \\\* scale + scale) - scale`.**

### \***`text\\\_center(channel: int, txt: str, y: int, scale: int = 1) -\\\> None`**

\***Renders the string horizontally centered on the display. The vertical position `y` is the top of the text.**

### \***`text\\\_fit(channel: int, txt: str, y: int, max\\\_scale: int = 3) -\\\> int`**

\***Tries scales from `max\\\_scale` down to 1 and picks the largest scale that makes the text fit within `display width - 8` pixels. Renders the text centered.**  
**Returns the scale that was actually used.**

## \***6. Internal Methods (not for public use)**

| \***Method** | \***Description** |
| :-: | :-: |
| \***`\\\_cmd(c)`** | \***Send a command byte** |
| \***`\\\_data(d)`** | \***Send data byte(s)** |
| \***`\\\_wait(timeout)`** | \***Poll BUSY pin until idle** |
| \***`\\\_reset()`** | \***Hardware reset pulse** |
| \***`\\\_buf(channel)`** | \***Return the underlying bytearray for BK or RD** |
| \***`\\\_get\\\_char(ch)`** | \***Extract 5 font bytes for a character** |


## \***7. Constants**

| \***Name** | \***Value** | \***Meaning** |
| :-: | :-: | :-: |
| \***`WHITE`** | \***0** | \***White (no ink)** |
| \***`BLACK`** | \***1** | \***Black ink** |
| \***`RED`** | \***2** | \***Red ink** |
| \***`BK`** | \***0** | \***Black channel** |
| \***`RD`** | \***1** | \***Red channel** |
| \***`W`** | \***128** | \***Physical width (pixels)** |
| \***`H`** | \***296** | \***Physical height (pixels)** |


## \***8. Timing & Dependencies**

- \***SPI baudrate: 2 MHz (safe for long wires, can be increased)**

- \***Typical refresh time: 2–3 seconds**

- \***Timeout for busy wait: 15 seconds (init) / 20 seconds (show)**

- \***Uses `machine.Pin`, `machine.SoftSPI`, `time` from MicroPython**

## \***9. Example: Complete Program**

**python**

```
\*\*\*from epaper2in9bv3 import EPaper29BV3\*\*  
  
\*\*\*import time\*\*  
  
  
\*\*\*ep = EPaper29BV3(rotation=0)\*\*  
  
\*\*\*ep.init()\*\*  
  
\*\*\*ep.clear()\*\*  
  
  
\*\*\*\\\# Draw a black circle and a red rectangle\*\*\*  
  
\*\*\*ep.circle(ep.BK, 64, 100, 40, filled=False)\*\*  
  
\*\*\*ep.fill\\\_rect(ep.RD, 20, 160, 88, 40)\*\*  
  
  
\*\*\*\\\# Centered text with automatic scaling\*\*\*  
  
\*\*\*ep.text\\\_fit(ep.BK, "Hello ePaper", 240, max\\\_scale=3)\*\*  
  
  
\*\*\*ep.show()\*\*  
  
\*\*\*time.sleep(5)\*\*  
  
\*\*\*ep.sleep()\*\*
```

## \***10. Revision History**

| \***Version** | \***Date** | \***Changes** |
| :-: | :-: | :-: |
| \***1.0** | \***2026‑04‑12** | \***Initial release**  |


