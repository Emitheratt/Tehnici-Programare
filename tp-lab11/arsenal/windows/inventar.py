
from dataclasses import dataclass, asdict
import json


CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}


# A1 - Clasa Proces
@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    # A2 - Verifica daca procesul este suspect
    def e_suspect(self):
        return any(cale in self.cale for cale in CAI_SUSPECTE)


# A3 - Clasa Eveniment
@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    # A4 - Verifica daca evenimentul este suspect
    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel == "critical"


# A5 - Incarca procesele din JSON
def incarca_procese(cale):
    with open(cale, encoding="utf-8") as f:
        date = json.load(f)

    return [Proces(**p) for p in date]


# A6 - Incarca evenimentele din JSON
def incarca_evenimente(cale):
    with open(cale, encoding="utf-8") as f:
        date = json.load(f)

    return [Eveniment(**e) for e in date]


# B1 - Clasa Inventar
@dataclass
class Inventar:
    procese: list
    evenimente: list

    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)], [])

    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self):
        grupuri = {}

        for p in self.procese:
            grupuri.setdefault(p.user, []).append(p.nume)

        return grupuri

    # B2 - Identifica procesele suspecte
    def procese_suspecte(self):
        return [p for p in self.procese if p.e_suspect()]

    # B3 - Identifica evenimentele suspecte
    def evenimente_suspecte(self):
        return [e for e in self.evenimente if e.e_suspect()]

    # B4 - Numara elementele suspecte
    def numara_suspecte(self):
        return {
            "procese": len(self.procese_suspecte()),
            "evenimente": len(self.evenimente_suspecte())
        }

    def raport_json(self):
        raport = {
            "procese": [asdict(p) for p in self.procese],
            "evenimente": [asdict(e) for e in self.evenimente],
            "suspecte": self.numara_suspecte()
        }

        return json.dumps(raport, indent=4)

def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = incarca_evenimente(a.capturi + "/evenimente.json")

    procese_suspecte = inv.suspecte()
    evenimente_alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        raport = {
            "procese_suspecte": [asdict(p) for p in procese_suspecte],
            "alarme": [asdict(e) for e in evenimente_alarma]
        }
        print(json.dumps(raport, indent=4))
    else:
        print(f"Procese: {len(inv)} | suspecte: {len(procese_suspecte)}")

        for p in procese_suspecte:
            print(f" [{p.pid}] {p.nume} ({p.user}) {p.cale}")

        print(f"Evenimente: {len(ev)} | alarma: {len(evenimente_alarma)}")

        for e in evenimente_alarma:
            print(f" {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")


if __name__ == "__main__":
    main()

