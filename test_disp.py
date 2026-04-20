# test_disp.py
# Visual test suite for epaper2in9bv3 driver
# Single screen, landscape mode, all features at once

from epaper2in9bv3 import EPaper29BV3
import screenshot

ep = EPaper29BV3(rotation=90)
ep.init()
ep.clear()

W = ep.width   # 296
H = ep.height  # 128

# ── Border ─────────────────────────────────────────────────────────────
ep.draw_rect(ep.BK, 0, 0, W, H)
ep.draw_rect(ep.BK, 2, 2, W - 4, H - 4)

# ── Title bar ──────────────────────────────────────────────────────────
ep.fill_rect(ep.BK, 3, 3, W - 6, 13)
ep.text_center(ep.BK, "epaper2in9bv3 driver test", 5)
for ly in range(3, 16):
    for lx in range(3, W - 3):
        px, py = ly, ep.H - 1 - lx
        if 0 <= px < ep.W and 0 <= py < ep.H:
            idx = (px + py * ep.W) // 8
            bit = 7 - (px % 8)
            val = (ep._bk[idx] >> bit) & 1
            if val == 1:
                ep.pixel(ep.BK, lx, ly)
            else:
                ep.pixel_off(ep.BK, lx, ly)
ep.hline(ep.BK, 3, 16, W - 6)

# ── Oddelovace stlpcov ─────────────────────────────────────────────────
# Col A: x=3  ..x=91   sirka=88
# Col B: x=92 ..x=195  sirka=103
# Col C: x=196..x=293  sirka=97
ep.vline(ep.BK, 92,  17, H - 19)
ep.vline(ep.BK, 196, 17, H - 19)

# ══ COL A – Shapes (y: 17-124) ════════════════════════════════════════
# y=18 nadpis, y=27 sep
# y=30..43 rects, y=48..71 circles, y=76..99 triangles, y=104..124 lines
ep.text(ep.BK, "Shapes", 4, 18)
ep.hline(ep.BK, 4, 27, 87)

ep.fill_rect(ep.BK,  4, 30, 22, 13)
ep.draw_rect(ep.BK, 30, 30, 22, 13)
ep.text(ep.BK, "fil", 6, 33)
ep.text(ep.BK, "drw", 32, 33)

ep.circle(ep.BK, 15, 56, 10)
ep.circle(ep.BK, 42, 56, 10, filled=True)
ep.text(ep.BK, "circ", 4, 69)

ep.triangle(ep.BK,  4, 92, 18, 76, 32, 92)
ep.triangle(ep.BK, 38, 92, 52, 76, 66, 92, filled=True)
ep.text(ep.BK, "tri", 4, 95)

ep.hline(ep.BK, 4, 106, 35)
ep.vline(ep.BK, 44, 103, 12)
ep.line(ep.BK,  52, 103, 88, 117)
ep.text(ep.BK, "lines", 4, 109)

# ══ COL B – Text (y: 17-124) ══════════════════════════════════════════
# y=18 nadpis, y=27 sep
# y=30 s1(7px→37), y=40 lbl, y=50 Hello! scale2(14px→64)
# y=68 lbl, y=77 Hi! scale3(21px→98)
# y=100 sep, y=102 centered(7px→109)
# y=111 sep, y=113 text_fit(7px→120)
ep.text(ep.BK, "Text", 97, 18)
ep.hline(ep.BK, 94, 27, 101)

ep.text(ep.BK, "s1: Hello World!", 94, 30)
ep.text(ep.BK, "scale 2:", 94, 40)
ep.text(ep.BK, "Hello!", 94, 50, scale=2)
ep.text(ep.BK, "scale 3:", 94, 68)
ep.text(ep.BK, "Hi!", 94, 77, scale=3)

ep.hline(ep.BK, 94, 100, 101)
cx = 94 + (101 - ep.text_width("centered")) // 2
ep.text(ep.BK, "centered", cx, 102)

ep.hline(ep.BK, 94, 111, 101)
cx2 = 94 + (101 - ep.text_width("text_fit")) // 2
ep.text(ep.BK, "text_fit", cx2, 115)

# ══ COL C – Red + pixel + clear_rect (y: 17-124) ══════════════════════
# y=18 nadpis, y=27 sep
# y=30..43 red shapes
# y=47 RED text, y=58..72 red2 scale2
# y=74 sep, y=76 pixel grid label, y=85..100 grid
# y=102 sep, y=104 clear_rect: label
# y=112 sep, y=113..119 blok+cleared
ep.text(ep.BK, "Red+misc", 200, 18)
ep.hline(ep.BK, 198, 27, 95)

ep.fill_rect(ep.RD, 199, 30, 26, 13)
ep.draw_rect(ep.RD, 230, 30, 26, 13)
ep.circle(ep.RD, 272, 36, 7, filled=True)

ep.text(ep.RD, "RED text", 199, 47)
ep.text(ep.RD, "red2", 199, 57, scale=2)

ep.hline(ep.BK, 198, 73, 95)
ep.text(ep.BK, "pixel grid:", 199, 75)
for y in range(84, 100, 3):
    for x in range(199, 291, 3):
        ep.pixel(ep.BK, x, y)

ep.hline(ep.BK, 198, 101, 95)
ep.text(ep.BK, "clear_rect:", 199, 103)

ep.hline(ep.BK, 198, 112, 95)
ep.fill_rect(ep.BK, 199, 113, 93, 12)  # cierny blok y=113..124 (cele pole)
ep.clear_rect(ep.BK, 215, 114, 60, 10) # biely vyrez y=114..123
ep.text(ep.BK, "cleared", 217, 115)    # text        y=115..121

# ── Screenshot + show ──────────────────────────────────────────────────
screenshot.capture(ep, "test_disp.bmp")
ep.show()
ep.sleep()
print("Done.")