import argparse
import base64
import hashlib
import json
import re
from urllib.parse import unquote


# ============================================================
# A1 - TEXT SI BYTES
# ============================================================

def demo_bytes():
    s = "Salut"
    b = s.encode()

    print("A1 - text:", s)
    print("A1 - bytes:", b)
    print("A1 - primul octet:", b[0])
    print("A1 - hex:", b.hex())

    refacut = bytes.fromhex(b.hex())
    print("A1 - bytes refacute:", refacut)


# ============================================================
# A2 - RECUNOASTEREA STRATULUI
# ============================================================

def ghici_strat(s):
    if not isinstance(s, str):
        return "necunoscut"

    # URL encoding
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"

    # HEX
    if (
        len(s) > 0
        and len(s) % 2 == 0
        and re.fullmatch(r"[0-9A-Fa-f]+", s)
    ):
        return "hex"

    # BASE64
    if (
        len(s) % 4 == 0
        and re.fullmatch(r"[A-Za-z0-9+/]*={0,2}", s)
    ):
        return "base64"

    return "necunoscut"


# ============================================================
# A3 - DECODAREA
# ============================================================

def desfa(s):
    strat = ghici_strat(s)

    try:
        if strat == "base64":
            rezultat = base64.b64decode(s, validate=True)
            return strat, rezultat

        if strat == "hex":
            rezultat = bytes.fromhex(s)
            return strat, rezultat

        if strat == "url":
            rezultat = unquote(s).encode()
            return strat, rezultat

    except Exception:
        pass

    return "necunoscut", s.encode()


# ============================================================
# A4 - TEXT CITIBIL
# ============================================================

def citibil(b):
    if not b:
        return False

    return all(32 <= c < 127 for c in b)


def decode_straturi(val, maxim=8):
    rezultate = []

    for _ in range(maxim):
        if not isinstance(val, str):
            break

        strat, b = desfa(val)

        if strat == "necunoscut":
            break

        rezultate.append({
            "strat": strat,
            "valoare": b.decode(errors="replace")
        })

        if citibil(b):
            return rezultate, b

        try:
            val = b.decode()
        except UnicodeDecodeError:
            break

    if rezultate:
        ultima = rezultate[-1]["valoare"].encode()

        if citibil(ultima):
            return rezultate, ultima

    return rezultate, val.encode() if isinstance(val, str) else val


# ============================================================
# A5 - XOR BRUTE FORCE
# ============================================================

def sparge_xor(cale):
    with open(cale, "rb") as f:
        date = f.read()

    rezultate = []

    for k in range(256):
        clar = bytes(b ^ k for b in date)

        if citibil(clar):
            try:
                text = clar.decode()
                rezultate.append((k, text))
            except UnicodeDecodeError:
                pass

    return rezultate


# ============================================================
# A6 - HASH
# ============================================================

def identifica_hash(tinta):
    lungime = len(tinta)

    if lungime == 32:
        return "md5"

    if lungime == 40:
        return "sha1"

    if lungime == 64:
        return "sha256"

    return "necunoscut"


def sparge_hash(cale_hash, cale_wordlist):
    with open(cale_hash, encoding="utf-8") as f:
        tinta = f.readline().strip()

    algoritm = identifica_hash(tinta)

    if algoritm == "necunoscut":
        return None, None, tinta

    with open(cale_wordlist, encoding="latin1") as f:
        for cuvant in f:
            cuvant = cuvant.strip()

            if algoritm == "md5":
                rezultat = hashlib.md5(
                    cuvant.encode()
                ).hexdigest()

            elif algoritm == "sha1":
                rezultat = hashlib.sha1(
                    cuvant.encode()
                ).hexdigest()

            else:
                rezultat = hashlib.sha256(
                    cuvant.encode()
                ).hexdigest()

            if rezultat == tinta:
                return algoritm, cuvant, tinta

    return algoritm, None, tinta


# ============================================================
# A7 - FISA JSON
# ============================================================

def salveaza_fisa(strat, rezultat, cale):
    date = {
        "strat": strat,
        "rezultat": rezultat
    }

    with open(cale, "w", encoding="utf-8") as f:
        json.dump(date, f, ensure_ascii=False, indent=4)


# ============================================================
# TEST / DEMO
# ============================================================

def demo():
    print("=" * 60)
    print("LABORATORUL 6 - LUCRAREA A")
    print("=" * 60)

    # A1
    demo_bytes()

    print("\nA2 - recunoastere:")
    teste = [
        "%2Fetc%2Fpasswd",
        "48656c6c6f",
        "U2FsdXQ="
    ]

    for x in teste:
        print(x, "->", ghici_strat(x))

    # A3
    print("\nA3 - decodare:")
    for x in teste:
        strat, rezultat = desfa(x)
        print(strat, "->", rezultat)

    # A4
    print("\nA4 - straturi multiple:")

    try:
        with open("probe/mesaj.txt", encoding="utf-8") as f:
            val = f.read().strip()

        print("Mesaj initial:", val)

        rezultate, final = decode_straturi(val)

        for r in rezultate:
            print(r["strat"], "->", r["valoare"])

        # Continuam decodarea daca rezultatul este inca Base64/Hex
        current = final

        for _ in range(10):
            try:
                text = current.decode("ascii").strip()
            except UnicodeDecodeError:
                break

            strat, rezultat = desfa(text)

            if strat == "necunoscut":
                break

            print(strat, "->", rezultat)

            current = rezultat

        print("Rezultat final:", current.decode(errors="replace"))

    except FileNotFoundError:
        print("probe/mesaj.txt nu exista.")

    # A5
    print("\nA5 - XOR:")

    try:
        rezultate_xor = sparge_xor("probe/xor.bin")

        for cheie, text in rezultate_xor:
            print("cheie:", cheie, "->", text)

    except FileNotFoundError:
        print("probe/xor.bin nu exista inca.")

    # A6
    print("\nA6 - HASH:")

    try:
        algoritm, parola, tinta = sparge_hash(
            "probe/hashuri.txt",
            "probe/wordlist.txt"
        )

        print("lungime:", len(tinta))
        print("algoritm:", algoritm)
        print("parola:", parola)

    except FileNotFoundError:
        print("hashuri.txt sau wordlist.txt lipseste.")

    # A7
    print("\nA7 - TEST BASE64:")

    strat, rezultat = desfa("U2FsdXQ=")

    print("strat:", strat)
    print("rezultat:", rezultat)

    salveaza_fisa(
        strat,
        rezultat.decode(errors="replace"),
        "arsenal/forensics/fisa.json"
    )

    print("fisa.json a fost salvata.")


# ============================================================
# ARGPARSE
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Decoder universal - Laboratorul 6"
    )

    parser.add_argument(
        "intrare",
        nargs="?",
        help="sirul care trebuie decodat"
    )

    parser.add_argument(
        "--fisier",
        action="store_true",
        help="trateaza intrarea ca fisier"
    )

    args = parser.parse_args()

    if args.intrare is None:
        demo()
        return

    if args.fisier:
        with open(args.intrare, "rb") as f:
            data = f.read()

        print("Fisier:", args.intrare)
        print("Bytes:", data)
        return

    strat, rezultat = desfa(args.intrare)

    print("Strat:", strat)
    print("Rezultat bytes:", rezultat)
    print(
        "Rezultat text:",
        rezultat.decode(errors="replace")
    )


if __name__ == "__main__":
    main()