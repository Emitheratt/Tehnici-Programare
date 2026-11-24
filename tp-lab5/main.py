import argparse
import csv

from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path

from webtools import (
    get_title,
    security_headers,
    DEFAULT_HEADERS
)

import webtools


# EXERCIȚIUL 44

print(
    "Ex. 44 - modul webtools importat."
)


# EXERCIȚIUL 45

# Dacă main.py ar avea propria funcție get_title,
# aceasta ar ascunde funcția importată.


# EXERCIȚIUL 46

print(
    "Ex. 46 - webtools:",
    webtools
)


# EXERCIȚIUL 47

print(
    "Ex. 47 - DEFAULT_HEADERS:",
    DEFAULT_HEADERS
)


# EXERCIȚIUL 48

parser = argparse.ArgumentParser(
    description="Raport despre un site web"
)

parser.add_argument(
    "url",
    help="URL-ul site-ului"
)

args = parser.parse_args()


response = webtools.fetch(
    args.url
)

if response is not None:

    print(
        "Ex. 48 - Titlu:",
        get_title(
            response.text
        )
    )

else:

    print(
        "Ex. 48 - site-ul nu a putut fi accesat"
    )


# EXERCIȚIUL 49

paths = [
    "/",
    "/robots.txt",
    "/sitemap.xml"
]

results = webtools.check_paths(
    args.url,
    paths
)

with open(
    Path(__file__).resolve().parent / "report.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "path",
            "status",
            "checked_at"
        ]
    )

    writer.writeheader()

    now = datetime.now().isoformat()

    for path, status in results.items():

        writer.writerow({

            "path":
                path,

            "status":
                status,

            "checked_at":
                now
        })


print(
    "Ex. 49 - report.csv creat."
)


# EXERCIȚIUL 50

report = webtools.site_report(
    args.url
)

print(
    f"\n=== Raport site: {args.url} ==="
)

print(
    "Cod de stare:",
    report["status_code"]
)

print(
    "Titlu:",
    report["title"]
)

print(
    "Adresă IP:",
    report["ip"]
)


if report["redirects"]:

    chain = " -> ".join(

        f'{item["status_code"]}'
        f' -> {item["url"]}'

        for item in report["redirects"]
    )

else:

    chain = (
        "Nicio redirecționare"
    )


print(
    "Redirecționări:",
    chain
)


print(
    "Scor securitate:",
    report[
        "security_score"
    ]
)


print(
    "Certificat:",
    report[
        "certificate_days_left"
    ],
    "zile rămase"
)


print(
    "Legături:",
    report[
        "internal_links"
    ],
    "interne,",
    report[
        "external_links"
    ],
    "externe"
)


print(
    "Căi interzise:",
    ", ".join(
        report[
            "disallowed_paths"
        ]
    )
    or "niciuna"
)


print(
    "Salvat în report.json"
)