
import re
import sys
from collections import Counter

# Tiparul pentru identificarea autentificarilor esuate
TIPAR = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from (\S+) port"
)


# A1 - Identifica o autentificare esuata
def esec(linie):
    m = TIPAR.search(linie)

    if m is None:
        return None

    return (m.group(1), m.group(2))


# A2 - Citeste toate esecurile din fisier
def citeste_esecuri(cale):
    esecuri = []

    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri

    with f:
        for linie in f:
            r = esec(linie)

            if r is not None:
                esecuri.append({
                    "user": r[0],
                    "ip": r[1]
                })

    return esecuri


# A3 - Numara esecurile pentru fiecare IP
def pe_ip(esecuri):
    return Counter(e["ip"] for e in esecuri)


# A4 - Functia principala
def main():
    if len(sys.argv) > 1:
        cale = sys.argv[1]
    else:
        cale = "arsenal/aparare/start/auth.log"

    esecuri = citeste_esecuri(cale)
    counts = pe_ip(esecuri)

    print("Esecuri de autentificare:", len(esecuri))

    for ip, n in counts.most_common():
        print(f"{ip}: {n}")


if __name__ == "__main__":
    main()
