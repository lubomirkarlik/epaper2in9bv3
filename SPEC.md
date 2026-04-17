\# Software Specification – Waveshare 2.9" e-Paper B V3 Driver



\*\*Driver version:\*\* 1.1  

\*\*Target platform:\*\* MicroPython (tested on ESP32‑S3 Zero)  

\*\*Display:\*\* 2.9 inch, 128×296 pixels, black/white/red, SPI interface



\## \*\*1. Initialisation \& Hardware\*\*



\### \*\*1.1 Constructor\*\*

`EPaper29BV3(cs=13, dc=12, rst=5, busy=11, clk=4, mosi=3, miso=16, rotation=0)`



\* \*\*MISO Pin\*\*: MicroPython `SoftSPI` vyžaduje definovanie MISO pinu, aj keď displej dáta neodosiela. Ak GPIO16 používate inak, priraďte voľný pin.

\* \*\*Rotation\*\*: Podporované uhly 0, 90, 180, 270.



\### \*\*1.2 Power Management\*\*

\* \*\*`init()`\*\*: Inicializuje radič. Volajte raz po zapnutí.

\* \*\*`sleep()`\*\*: Vstúpi do hlbokého spánku. Nutné volať pred odpojením napájania.

\* \*\*`show()`\*\*: Prenesie buffery a obnoví displej. Blokuje vykonávanie programu.



\## \*\*2. Colour \& Drawing\*\*



\### \*\*Constants\*\*

\* `WHITE` (0), `BLACK` (1), `RED` (2)

\* `BK` (0 - čierny kanál), `RD` (1 - červený kanál)



\### \*\*`fill(color: int)`\*\*

\* `WHITE (0)`: Vymaže oba kanály na bielo.

\* `BLACK (1)`: Zaplní čierny kanál (červený zostáva).

\* `RED (2)`: Zaplní červený kanál (čierny zostáva).



\## \*\*3. Text Rendering\*\*



\* \*\*Font\*\*: Monospace 5×7 pixelov.

\* \*\*Rozsah\*\*: ASCII 32–122.

\* \*\*Špeciálne znaky\*\*: Podpora pre symbol stupňa (`°`) cez kód `0xB0`.

\* \*\*`text\_fit()`\*\*: Automaticky zvolí najväčšiu mierku (max\_scale), ktorá sa zmestí na šírku.



\## \*\*4. Error Handling\*\*



\* \*\*RuntimeError\*\*: Metódy `\_wait()` (a tým pádom `init()` a `show()`) vyvolajú výnimku, ak BUSY pin zostane v stave HIGH dlhšie ako timeout (15-20s). Toto indikuje chybu hardvéru alebo zapojenia.



\## \*\*5. Example\*\*



```python

from epaper2in9bv3 import EPaper29BV3

ep = EPaper29BV3(rotation=90)

ep.init()

ep.clear()

ep.text\_center(ep.BK, "Teplota: 24°C", 50, scale=2)

ep.show()

ep.sleep()

