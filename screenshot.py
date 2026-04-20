# screenshot.py – vytvorí BMP screenshot z e-paper displeja 2.9" B V3
# Použitie v REPL:
#   from epaper2in9bv3 import EPaper29BV3
#   ep = EPaper29BV3()
#   ep.init()
#   ... (vykreslite obsah) ...
#   import screenshot
#   screenshot.capture(ep)                # uloží screenshot.bmp
#   screenshot.capture(ep, 'obrazok.bmp') # vlastný názov

import struct

def capture(ep, filename='screenshot.bmp'):
    """
    Vytvorí BMP súbor z aktuálneho framebufferu displeja.
    
    Args:
        ep: inštancia EPaper29BV3 (musí byť už inicializovaná)
        filename: názov výstupného súboru (predvolene screenshot.bmp)
    
    Returns:
        True ak úspešné, inak False
    """
    try:
        # Získanie framebufferov a rozmerov displeja
        # Displej má fyzické rozmery 128 x 296 pixelov (natívna orientácia)
        width = ep.W   # 128
        height = ep.H  # 296
        bk_buffer = ep._bk  # bytearray pre čierny kanál
        
        # Konverzia framebufferu na BMP
        bmp_data = _framebuffer_to_bmp(bk_buffer, width, height)
        
        # Zápis do súboru
        with open(filename, 'wb') as f:
            f.write(bmp_data)
        
        print(f"Screenshot uložený ako {filename} ({len(bmp_data)} bajtov)")
        return True
    except Exception as e:
        print(f"Chyba pri vytváraní screenshotu: {e}")
        return False

def _framebuffer_to_bmp(fb, width, height):
    """
    Konvertuje monochromatický framebuffer (1 bit per pixel, MSB prvý)
    na BMP súbor.
    
    Formát framebufferu: riadok po riadku, každý riadok má (width+7)//8 bajtov,
    bit 7 (MSB) = prvý pixel v riadku.
    """
    row_bytes = (width + 7) // 8
    # BMP vyžaduje zarovnanie každého riadku na 4 bajty
    padding = (4 - (row_bytes % 4)) % 4
    image_data_size = (row_bytes + padding) * height
    file_size = 14 + 40 + image_data_size
    
    # ----- BMP hlavička (14 bajtov) -----
    bmp_header = struct.pack('<HIHHIIIIII',
        0x4D42,          # 'BM'
        file_size,       # celková veľkosť súboru
        0, 0,            # rezervované
        14 + 40,         # offset začiatku obrazových dát
    )
    
    # ----- DIB hlavička (40 bajtov) -----
    dib_header = struct.pack('<IIIHHIIIIII',
        40,              # veľkosť DIB hlavičky
        width,           # šírka v pixeloch
        height,          # výška v pixeloch
        1,               # počet rovin
        1,               # bity na pixel (1 = monochromatický)
        0,               # kompresia (0 = žiadna)
        image_data_size, # veľkosť obrazových dát
        2835, 2835,      # rozlíšenie (72 DPI)
        0, 0             # počet farieb v palete (0 = 2^1)
    )
    
    # ----- Obrazové dáta -----
    # Prevod z formátu framebufferu (bit 7 = prvý pixel) do BMP (bit 7 = prvý pixel)
    # BMP očakáva rovnaké poradie, takže netreba invertovať bity.
    # Ale BMP ukladá riadky zdola nahor, zatiaľ čo framebuffer je zhora nadol.
    # Preto riadky otočíme.
    image_data = bytearray(image_data_size)
    for y in range(height):
        src_start = y * row_bytes
        src_row = fb[src_start:src_start + row_bytes]
        # Cieľový riadok (opačné poradie)
        dst_y = height - 1 - y
        dst_start = dst_y * (row_bytes + padding)
        # Kopírovanie riadku
        image_data[dst_start:dst_start + row_bytes] = src_row
        # Zvyšok (padding) zostáva 0
    
    return bmp_header + dib_header + image_data

# Ak chcete spustiť skript priamo (napr. exec(open('screenshot.py').read()))
if __name__ == "__main__":
    # Pokúsime sa nájsť globálnu premennú 'ep' (inštancia displeja)
    ep = globals().get('ep')
    if ep is None:
        print("Premenná 'ep' nie je definovaná. Najskôr vytvorte inštanciu EPaper29BV3.")
        print("Príklad:")
        print("  from epaper2in9bv3 import EPaper29BV3")
        print("  ep = EPaper29BV3()")
        print("  ep.init()")
        print("  ... vykreslite ...")
        print("  import screenshot")
        print("  screenshot.capture(ep)")
    else:
        capture(ep)
        