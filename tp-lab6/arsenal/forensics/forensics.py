import sys
import re
import zipfile
from PIL import Image
from pathlib import Path


def magic_bytes(cale):
    """B1 - identifică tipul fișierului după magic bytes."""
    with open(cale, "rb") as f:
        data = f.read(16)

    if data.startswith(b"\xFF\xD8\xFF"):
        return "JPEG"

    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG"

    if data.startswith(b"PK\x03\x04"):
        return "ZIP"

    return "Necunoscut"


def strings(cale, minim=4):
    """B2 - extrage secvențele ASCII lizibile."""
    with open(cale, "rb") as f:
        data = f.read()

    pattern = rb"[\x20-\x7e]{%d,}" % minim
    return [
        x.decode("ascii", errors="replace")
        for x in re.findall(pattern, data)
    ]


def exif(cale):
    """B3 - extrage informațiile EXIF."""
    img = Image.open(cale)
    rezultat = {}

    exif_data = img.getexif()

    for tag_id, value in exif_data.items():
        rezultat[str(tag_id)] = value

    return rezultat


def carve_zip(cale, iesire="carved"):
    """B4 - caută un ZIP ascuns la sfârșitul fișierului."""
    with open(cale, "rb") as f:
        data = f.read()

    pozitie = data.find(b"PK\x03\x04")

    if pozitie == -1:
        return None

    Path(iesire).mkdir(exist_ok=True)

    zip_path = Path(iesire) / "extras.zip"

    with open(zip_path, "wb") as f:
        f.write(data[pozitie:])

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(iesire)

    return str(zip_path)


def main():
    if len(sys.argv) < 2:
        print("Utilizare:")
        print("python forensics.py <fisier>")
        return

    cale = sys.argv[1]

    print("=" * 60)
    print("LABORATORUL 6 - FORENSICS")
    print("=" * 60)

    print("\nB1 - MAGIC BYTES:")
    print(magic_bytes(cale))

    print("\nB2 - STRINGS:")
    for s in strings(cale):
        print(s)

    print("\nB3 - EXIF:")
    try:
        info = exif(cale)

        for key, value in info.items():
            print(key, "->", value)

    except Exception as e:
        print("Nu s-au putut citi EXIF:", e)

    print("\nB4 - CARVING ZIP:")
    rezultat = carve_zip(cale)

    if rezultat:
        print("ZIP găsit:", rezultat)
    else:
        print("Nu a fost găsit ZIP.")


if __name__ == "__main__":
    main()