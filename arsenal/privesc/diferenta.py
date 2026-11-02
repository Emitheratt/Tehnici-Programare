from arsenal.privesc.enumerare import citeste_linii, nume, GTFO


def cai(fisier):
    return set(citeste_linii(fisier))

baza = cai("arsenal/privesc/start/baza_suid.txt")
acum = cai("arsenal/privesc/start/suid.txt")

noi = acum - baza

print("SUID în baza de referință:", len(baza))
print("SUID actuale:", len(acum))
print("SUID noi:", len(noi))
print("Căi noi:", sorted(noi))

riscuri = {
    cale: "mare" if nume(cale) in GTFO else "normal"
    for cale in noi
}

periculoase = [
    cale for cale in noi
    if riscuri[cale] == "mare"
]

print("Riscuri pentru programele noi:", riscuri)
print("periculoase NOI:", sorted(periculoase))