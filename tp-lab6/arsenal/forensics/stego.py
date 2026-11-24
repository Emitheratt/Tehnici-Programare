from PIL import Image


def ascunde_lsb(input_path, output_path, mesaj):
    """
    B5 - ascunde un mesaj într-o imagine folosind ultimul bit
    al canalelor RGB.
    """

    img = Image.open(input_path).convert("RGB")

    # Marcăm sfârșitul mesajului cu 8 zerouri
    mesaj = mesaj + "\0"

    # Transformăm mesajul în biți
    biti = ""

    for caracter in mesaj:
        biti += format(ord(caracter), "08b")

    pixeli = list(img.getdata())

    if len(biti) > len(pixeli) * 3:
        raise ValueError("Mesajul este prea mare pentru imagine.")

    index = 0
    pixeli_noi = []

    for r, g, b in pixeli:

        canale = [r, g, b]

        for i in range(3):
            if index < len(biti):
                # Înlocuim ultimul bit
                canale[i] = (canale[i] & 0xFE) | int(biti[index])
                index += 1

        pixeli_noi.append(tuple(canale))

    img.putdata(pixeli_noi)
    img.save(output_path)

    print("Mesaj ascuns în:", output_path)


def extrage_lsb(input_path):
    """
    B6 - extrage mesajul ascuns în ultimii biți ai canalelor RGB.
    """

    img = Image.open(input_path).convert("RGB")

    biti = ""

    for r, g, b in img.getdata():
        biti += str(r & 1)
        biti += str(g & 1)
        biti += str(b & 1)

    mesaj = ""

    for i in range(0, len(biti), 8):
        byte = biti[i:i + 8]

        if len(byte) < 8:
            break

        valoare = int(byte, 2)

        if valoare == 0:
            break

        mesaj += chr(valoare)

    return mesaj


def main():
    print("=" * 60)
    print("LABORATORUL 6 - STEGANOGRAFIE LSB")
    print("=" * 60)

    imagine_intrare = "probe/ascuns.png"
    imagine_iesire = "probe/ascuns_lsb.png"

    mesaj = "FLAG{steganografie_lsb}"

    print("\nB5 - ASCUNDERE LSB:")
    print("Mesaj:", mesaj)

    ascunde_lsb(
        imagine_intrare,
        imagine_iesire,
        mesaj
    )

    print("\nB6 - EXTRAGERE LSB:")

    rezultat = extrage_lsb(imagine_iesire)

    print("Mesaj extras:", rezultat)


if __name__ == "__main__":
    main()