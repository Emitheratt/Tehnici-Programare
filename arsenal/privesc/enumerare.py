
import argparse
import json
import os


def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        return [
            linie.strip()
            for linie in f
            if linie.strip() and not linie.strip().startswith("#")
        ]


def nume(cale):
    return cale.rsplit("/", 1)[-1]


GTFO = {
    "find", "vim.basic", "vim", "nmap", "cp",
    "bash", "less", "awk", "python3", "perl"
}


def suid_constatari(cale):
    rezultate = []

    for c in citeste_linii(cale):
        nume_fisier = nume(c)

        rezultate.append({
            "cale": c,
            "nume": nume_fisier,
            "risc": "mare" if nume_fisier in GTFO else "normal"
        })

    return rezultate


def sudo_constatari(cale):
    rezultate = []

    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)

        rezultate.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal"
        })

    return rezultate


def cron_constatari(cale):
    rezultate = []

    for ln in citeste_linii(cale):
        campuri = ln.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])

        rezultate.append({
            "user": user,
            "comanda": comanda
        })

    return rezultate


def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt"))
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("capturi")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    raport = enumereaza(args.capturi)

    if args.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    for categorie, rezultate in raport.items():
        risc_mare = sum(
            1 for x in rezultate if x.get("risc") == "mare"
        )
        print(
            f"{categorie}: {len(rezultate)} gasite, "
            f"{risc_mare} cu risc mare"
        )

    utilizatori_sudo = {x["user"] for x in raport["sudo"]}
    utilizatori_cron = {x["user"] for x in raport["cron"]}
    utilizatori = sorted(utilizatori_sudo | utilizatori_cron)

    print("utilizatori implicati:", ", ".join(utilizatori))

    with open("arsenal/privesc/enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)

    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()