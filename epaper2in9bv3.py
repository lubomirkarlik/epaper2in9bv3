# epaper2in9bv3.py
# MicroPython driver for Waveshare 2.9inch e-Paper B V3 (black/white/red)
# Tested on ESP32-S3 Zero
# Resolution: 128 x 296 pixels
# BUSY pin logic: 1 = busy, 0 = idle
#
# Wiring:
#   BUSY -> GPIO11
#   RST  -> GPIO5
#   D/C  -> GPIO12
#   CS   -> GPIO13
#   CLK  -> GPIO4
#   MOSI -> GPIO3
#
# Basic usage:
#   from epaper2in9bv3 import EPaper29BV3
#   ep = EPaper29BV3()
#   ep.init()
#   ep.clear()
#   ep.text(ep.BK, "Hello!", 4, 10, scale=2)
#   ep.show()
#   ep.sleep()

from machine import Pin, SoftSPI
import time

# 5x7 pixel font, ASCII 32-122, each character = 5 column bytes, bit0 = top row
_FONT = b'\x00\x00\x00\x00\x00\x00\x5F\x00\x00\x00\x00\x07\x00\x07\x00\x14\x7F\x14\x7F\x14\x24\x2A\x7F\x2A\x12\x23\x13\x08\x64\x62\x36\x49\x55\x22\x50\x00\x05\x03\x00\x00\x00\x1C\x22\x41\x00\x00\x41\x22\x1C\x00\x08\x2A\x1C\x2A\x08\x08\x08\x3E\x08\x08\x00\x50\x30\x00\x00\x08\x08\x08\x08\x08\x00\x60\x60\x00\x00\x20\x10\x08\x04\x02\x3E\x51\x49\x45\x3E\x00\x42\x7F\x40\x00\x42\x61\x51\x49\x46\x21\x41\x45\x4B\x31\x18\x14\x12\x7F\x10\x27\x45\x45\x45\x39\x3C\x4A\x49\x49\x30\x01\x71\x09\x05\x03\x36\x49\x49\x49\x36\x06\x49\x49\x29\x1E\x00\x36\x36\x00\x00\x00\x56\x36\x00\x00\x00\x08\x14\x22\x41\x14\x14\x14\x14\x14\x41\x22\x14\x08\x00\x02\x01\x51\x09\x06\x32\x49\x79\x41\x3E\x7E\x11\x11\x11\x7E\x7F\x49\x49\x49\x36\x3E\x41\x41\x41\x22\x7F\x41\x41\x22\x1C\x7F\x49\x49\x49\x41\x7F\x09\x09\x09\x01\x3E\x41\x49\x49\x3A\x7F\x08\x08\x08\x7F\x00\x41\x7F\x41\x00\x20\x40\x41\x3F\x01\x7F\x08\x14\x22\x41\x7F\x40\x40\x40\x40\x7F\x02\x0C\x02\x7F\x7F\x04\x08\x10\x7F\x3E\x41\x41\x41\x3E\x7F\x09\x09\x09\x06\x3E\x41\x51\x21\x5E\x7F\x09\x19\x29\x46\x46\x49\x49\x49\x31\x01\x01\x7F\x01\x01\x3F\x40\x40\x40\x3F\x1F\x20\x40\x20\x1F\x3F\x40\x38\x40\x3F\x63\x14\x08\x14\x63\x07\x08\x70\x08\x07\x61\x51\x49\x45\x43\x00\x7F\x41\x41\x00\x02\x04\x08\x10\x20\x00\x41\x41\x7F\x00\x04\x02\x01\x02\x04\x40\x40\x40\x40\x40\x00\x01\x02\x04\x00\x20\x54\x54\x54\x78\x7F\x48\x44\x44\x38\x38\x44\x44\x44\x20\x38\x44\x44\x48\x7F\x38\x54\x54\x54\x18\x08\x7E\x09\x01\x02\x0C\x52\x52\x52\x3E\x7F\x08\x04\x04\x78\x00\x44\x7D\x40\x00\x20\x40\x44\x3D\x00\x7F\x10\x28\x44\x00\x00\x41\x7F\x40\x00\x7C\x04\x18\x04\x7C\x7C\x08\x04\x04\x78\x38\x44\x44\x44\x38\x7C\x14\x14\x14\x08\x08\x14\x14\x18\x7C\x7C\x08\x04\x04\x08\x48\x54\x54\x54\x20\x04\x3F\x44\x40\x20\x3C\x40\x40\x20\x7C\x1C\x20\x40\x20\x1C\x3C\x40\x30\x40\x3C\x44\x28\x10\x28\x44\x0C\x50\x50\x50\x3C\x44\x64\x54\x4C\x44\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x09\x09\x06\x00'


class EPaper29BV3:

    # Color constants
    WHITE = const(0)
    BLACK = const(1)
    RED   = const(2)

    # Channel selection
    BK = const(0)   # black channel
    RD = const(1)   # red channel

    # Physical display dimensions (always portrait, fixed)
    W = const(128)
    H = const(296)

    def __init__(self, cs=13, dc=12, rst=5, busy=11, clk=4, mosi=3, miso=16, rotation=0):
        """
        Initialize the driver.

        Args:
            cs:       Chip Select pin (default 13)
            dc:       Data/Command pin (default 12)
            rst:      Reset pin (default 5)
            busy:     Busy pin (default 11)
            clk:      SPI clock pin (default 4)
            mosi:     SPI MOSI pin (default 3)
            miso:     SPI MISO pin, not used by display (default 16)
            rotation: Display rotation in degrees: 0, 90, 180, 270 (default 0)
        """
        self._cs   = Pin(cs,   Pin.OUT, value=1)
        self._dc   = Pin(dc,   Pin.OUT, value=0)
        self._rst  = Pin(rst,  Pin.OUT, value=1)
        self._busy = Pin(busy, Pin.IN)
        self._spi  = SoftSPI(baudrate=2000000,
                             sck=Pin(clk), mosi=Pin(mosi), miso=Pin(miso))
        self.rotation  = rotation
        self._buf_size = self.W * self.H // 8
        self._bk = bytearray([0xFF] * self._buf_size)
        self._rd = bytearray([0xFF] * self._buf_size)

    # ── Logical dimensions (swap W/H for landscape rotations) ─────────
    @property
    def width(self):
        """Logical width in pixels (respects rotation)."""
        return self.H if self.rotation in (90, 270) else self.W

    @property
    def height(self):
        """Logical height in pixels (respects rotation)."""
        return self.W if self.rotation in (90, 270) else self.H

    # ── Low-level SPI communication ────────────────────────────────────
    def _cmd(self, c):
        self._dc.value(0)
        self._cs.value(0)
        self._spi.write(bytearray([c]))
        self._cs.value(1)

    def _data(self, d):
        self._dc.value(1)
        self._cs.value(0)
        self._spi.write(d if isinstance(d, (bytes, bytearray)) else bytearray([d]))
        self._cs.value(1)

    def _wait(self, timeout=15000):
        """Wait until BUSY pin goes low (idle). Returns False on timeout."""
        start = time.ticks_ms()
        while self._busy.value() == 1:
            if time.ticks_diff(time.ticks_ms(), start) > timeout:
                return False
            time.sleep_ms(10)
        time.sleep_ms(200)
        return True

    def _reset(self):
        """Hardware reset sequence."""
        self._rst.value(1); time.sleep_ms(200)
        self._rst.value(0); time.sleep_ms(5)
        self._rst.value(1); time.sleep_ms(200)

    def _buf(self, channel):
        """Return the framebuffer for the given channel (BK or RD)."""
        return self._bk if channel == self.BK else self._rd

    # ── Display control ────────────────────────────────────────────────
    def init(self):
        """Initialize the display. Must be called once after power-on."""
        self._reset()
        self._cmd(0x04); self._wait()
        self._cmd(0x00); self._data(bytearray([0x0F, 0x89]))
        self._cmd(0x61); self._data(bytearray([0x80, 0x01, 0x28]))
        self._cmd(0x50); self._data(bytearray([0x77]))

    def show(self):
        """Send both framebuffers to the display and trigger a full refresh."""
        self._cmd(0x10); self._data(self._bk); self._cmd(0x92)
        self._cmd(0x13); self._data(self._rd); self._cmd(0x92)
        self._cmd(0x12); self._wait(20000)

    def sleep(self):
        """Put the display into deep sleep. Call before cutting power."""
        self._cmd(0x02); self._wait()
        self._cmd(0x07); self._data(bytearray([0xA5]))

    def clear(self):
        """Clear both framebuffers to white (all 0xFF)."""
        for i in range(self._buf_size):
            self._bk[i] = 0xFF
            self._rd[i] = 0xFF

    # ── Pixel with rotation support ────────────────────────────────────
    def pixel(self, channel, x, y):
        """
        Set a single pixel in the given channel.

        Applies the current rotation before writing to the framebuffer.
        0 = black (for BK channel) or red (for RD channel).

        Args:
            channel: BK or RD
            x:       logical x coordinate
            y:       logical y coordinate
        """
        r = self.rotation
        if r == 0:
            x = self.W - 1 - x
            y = self.H - 1 - y
        elif r == 90:
            x, y = y, self.H - 1 - x
        elif r == 180:
            pass   # no transform = 180 degrees relative to rotation=0
        elif r == 270:
            x, y = self.W - 1 - y, x
        if 0 <= x < self.W and 0 <= y < self.H:
            self._buf(channel)[(x + y * self.W) // 8] &= ~(1 << (7 - (x % 8)))

    def pixel_off(self, channel, x, y):
        """
        Clear a single pixel (set to white) in the given channel.

        Applies the current rotation before writing to the framebuffer.

        Args:
            channel: BK or RD
            x:       logical x coordinate
            y:       logical y coordinate
        """
        r = self.rotation
        if r == 0:
            x = self.W - 1 - x
            y = self.H - 1 - y
        elif r == 90:
            x, y = y, self.H - 1 - x
        elif r == 180:
            pass
        elif r == 270:
            x, y = self.W - 1 - y, x
        if 0 <= x < self.W and 0 <= y < self.H:
            self._buf(channel)[(x + y * self.W) // 8] |= (1 << (7 - (x % 8)))

    # ── Drawing primitives ─────────────────────────────────────────────
    def fill(self, color):
        """
        Fill the entire display with a single color.

        Args:
            color: WHITE, BLACK, or RED
        """
        if color == self.WHITE:
            self.clear()
        elif color == self.BLACK:
            for i in range(self._buf_size): self._bk[i] = 0x00
        elif color == self.RED:
            for i in range(self._buf_size): self._rd[i] = 0x00

    def fill_rect(self, channel, x, y, w, h):
        """
        Draw a filled rectangle.

        Args:
            channel: BK or RD
            x, y:    top-left corner (logical coordinates)
            w, h:    width and height in pixels
        """
        for dy in range(h):
            for dx in range(w):
                self.pixel(channel, x + dx, y + dy)


    def clear_rect(self, channel, x, y, w, h):
        """
        Clear a rectangle to white.

        Args:
            channel: BK or RD
            x, y:    top-left corner (logical coordinates)
            w, h:    width and height in pixels
        """
        for dy in range(h):
            for dx in range(w):
                self.pixel_off(channel, x + dx, y + dy)

    def draw_rect(self, channel, x, y, w, h):
        """
        Draw a rectangle outline (no fill).

        Args:
            channel: BK or RD
            x, y:    top-left corner (logical coordinates)
            w, h:    width and height in pixels
        """
        self.hline(channel, x, y, w)
        self.hline(channel, x, y + h - 1, w)
        self.vline(channel, x, y, h)
        self.vline(channel, x + w - 1, y, h)

    def hline(self, channel, x, y, length):
        """
        Draw a horizontal line.

        Args:
            channel: BK or RD
            x, y:    start position
            length:  number of pixels
        """
        for i in range(length):
            self.pixel(channel, x + i, y)

    def vline(self, channel, x, y, length):
        """
        Draw a vertical line.

        Args:
            channel: BK or RD
            x, y:    start position
            length:  number of pixels
        """
        for i in range(length):
            self.pixel(channel, x, y + i)

    def line(self, channel, x0, y0, x1, y1):
        """
        Draw a line between two points using Bresenham's algorithm.

        Args:
            channel:     BK or RD
            x0, y0:      start point
            x1, y1:      end point
        """
        dx = abs(x1 - x0); dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.pixel(channel, x0, y0)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x0 += sx
            if e2 <  dx: err += dx; y0 += sy

    def circle(self, channel, x0, y0, r, filled=False):
        """
        Draw a circle or filled disk.

        Args:
            channel: BK or RD
            x0, y0:  center point
            r:       radius in pixels
            filled:  True for filled disk, False for outline only
        """
        x, y, err = r, 0, 3 - 2 * r
        while x >= y:
            if filled:
                self.hline(channel, x0 - x, y0 + y, 2 * x + 1)
                self.hline(channel, x0 - x, y0 - y, 2 * x + 1)
                self.hline(channel, x0 - y, y0 + x, 2 * y + 1)
                self.hline(channel, x0 - y, y0 - x, 2 * y + 1)
            else:
                for px, py in [(x,y),(-x,y),(x,-y),(-x,-y),
                               (y,x),(-y,x),(y,-x),(-y,-x)]:
                    self.pixel(channel, x0 + px, y0 + py)
            y += 1
            if err > 0:
                x -= 1
                err += 4 * (y - x) - 2
            else:
                err += 4 * y - 2

    def triangle(self, channel, x0, y0, x1, y1, x2, y2, filled=False):
        """
        Draw a triangle.

        Args:
            channel:            BK or RD
            x0,y0/x1,y1/x2,y2: three vertices
            filled:             True for filled triangle, False for outline only
        """
        if filled:
            pts = sorted([(y0, x0), (y1, x1), (y2, x2)])
            (ay, ax), (by, bx), (cy, cx) = pts
            for y in range(ay, cy + 1):
                if y < by:
                    xa = ax + (bx - ax) * (y - ay) // (by - ay) if by != ay else ax
                    xc = ax + (cx - ax) * (y - ay) // (cy - ay) if cy != ay else ax
                else:
                    xa = bx + (cx - bx) * (y - by) // (cy - by) if cy != by else bx
                    xc = ax + (cx - ax) * (y - ay) // (cy - ay) if cy != ay else ax
                self.hline(channel, min(xa, xc), y, abs(xc - xa) + 1)
        else:
            self.line(channel, x0, y0, x1, y1)
            self.line(channel, x1, y1, x2, y2)
            self.line(channel, x2, y2, x0, y0)

    # ── Text rendering ─────────────────────────────────────────────────
    def _get_char(self, ch):
        """Return 5 column bytes for the given character from the font table."""
        c = ord(ch)
        if c == 0xB0:   # degree sign ° -> mapped to position 127 in extended font
            c = 127
        if c < 32 or c > 127:
            c = 32   # unsupported characters rendered as space
        i = (c - 32) * 5
        return _FONT[i:i + 5]

    def char(self, channel, x, y, ch, scale=1):
        """
        Render a single character.

        Args:
            channel: BK or RD
            x, y:    top-left position
            ch:      character to render (ASCII 32-122)
            scale:   pixel scale factor (1 = 5x7px, 2 = 10x14px, ...)

        Returns:
            x position after the character (ready for the next character)
        """
        cols = self._get_char(ch)
        for ci in range(5):
            cb = cols[ci]
            for ri in range(7):
                if cb & (1 << ri):
                    for sx in range(scale):
                        for sy in range(scale):
                            self.pixel(channel, x + ci * scale + sx,
                                                y + ri * scale + sy)
        return x + 5 * scale + scale

    def text(self, channel, txt, x, y, scale=1):
        """
        Render a string of characters.

        Supported characters: ASCII 32-122 (space, digits, upper and lower case
        letters, common punctuation). Unsupported characters are rendered as space.

        Args:
            channel: BK or RD
            txt:     string to render
            x, y:    top-left position of first character
            scale:   pixel scale factor (1 = 5x7px, 2 = 10x14px, ...)
        """
        cx = x
        for ch in txt:
            cx = self.char(channel, cx, y, ch, scale)

    def text_width(self, txt, scale=1):
        """
        Calculate the pixel width of a string.

        Args:
            txt:   string to measure
            scale: pixel scale factor

        Returns:
            Width in pixels (no trailing inter-character gap)
        """
        return len(txt) * (5 * scale + scale) - scale

    def text_center(self, channel, txt, y, scale=1):
        """
        Render a string horizontally centered on the display.

        Args:
            channel: BK or RD
            txt:     string to render
            y:       vertical position
            scale:   pixel scale factor
        """
        x = (self.width - self.text_width(txt, scale)) // 2
        self.text(channel, txt, x, y, scale)

    def text_fit(self, channel, txt, y, max_scale=3):
        """
        Render a string at the largest scale that fits the display width.

        Tries scales from max_scale down to 1 and picks the first that fits
        within (display width - 8px margins).

        Args:
            channel:   BK or RD
            txt:       string to render
            y:         vertical position
            max_scale: maximum scale to try (default 3)

        Returns:
            Scale that was actually used
        """
        for scale in range(max_scale, 0, -1):
            w = self.text_width(txt, scale)
            if w <= self.width - 8:
                x = (self.width - w) // 2
                self.text(channel, txt, x, y, scale)
                return scale
        return 1