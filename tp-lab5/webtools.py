import time
import requests
import re
import hashlib
import json
import socket
import ssl
import datetime

from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser
from pathlib import Path


BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

DEFAULT_HEADERS = {
    "User-Agent": "WebLab-Emilia"
}


SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy"
]


def fetch(url, timeout=TIMEOUT):
    """Descarcă URL-ul și returnează răspunsul."""

    try:

        return requests.get(
            url,
            timeout=timeout,
            headers=DEFAULT_HEADERS
        )

    except requests.RequestException as e:

        print("Eroare fetch:", e)

        return None


def get_status(url):
    """Returnează codul HTTP."""

    response = fetch(url)

    if response is None:
        return None

    return response.status_code


def get_title(html):
    """Returnează titlul paginii."""

    start = html.find("<title>")

    if start == -1:
        return ""

    start += len("<title>")

    end = html.find(
        "</title>",
        start
    )

    if end == -1:
        return ""

    return html[
        start:end
    ].strip()


def security_headers(url):
    """Verifică antetele de securitate."""

    response = fetch(url)

    if response is None:

        return {
            name: False
            for name in SECURITY_HEADERS
        }

    return {
        name: name in response.headers
        for name in SECURITY_HEADERS
    }


def score_headers(results):
    """Calculează scorul antetelor."""

    return (
        f"{sum(results.values())}/"
        f"{len(results)}"
    )


def check_paths(base, paths):
    """Returnează codurile HTTP."""

    result = {}

    for path in paths:

        try:

            response = fetch(
                urljoin(
                    base,
                    path
                )
            )

            result[path] = (
                response.status_code
                if response
                else None
            )

        except requests.RequestException:

            result[path] = None

        time.sleep(1)

    return result


def fetch_robots(base):
    """Returnează robots.txt."""

    try:

        response = fetch(
            urljoin(
                base.rstrip("/") + "/",
                "robots.txt"
            )
        )

        if response is None:
            return None

        if response.status_code == 404:
            return None

        response.raise_for_status()

        return response.text

    except requests.RequestException:

        return None


def disallowed_paths(robots_text):
    """Extrage valorile Disallow."""

    if robots_text is None:
        return []

    result = []

    for line in robots_text.splitlines():

        line = line.strip()

        if line.lower().startswith(
            "disallow:"
        ):

            result.append(
                line.split(
                    ":",
                    1
                )[1].strip()
            )

    return result


def extract_links(html):
    """Extrage linkurile href."""

    return list(
        dict.fromkeys(
            re.findall(
                r'href=["\']([^"\']+)["\']',
                html
            )
        )
    )


def split_links(
    links,
    domain
):
    """Separă linkurile interne și externe."""

    internal = []

    external = []

    for link in links:

        full = urljoin(
            BASE_URL,
            link
        )

        if (
            urlparse(full).netloc
            == domain
        ):

            internal.append(link)

        else:

            external.append(link)

    return internal, external


def page_fingerprint(url):
    """Returnează hash-ul SHA-256."""

    response = fetch(url)

    if response is None:
        return None

    return hashlib.sha256(
        response.content
    ).hexdigest()


def resolve(hostname):
    """Returnează adresa IPv4."""

    try:

        return socket.gethostbyname(
            hostname
        )

    except socket.gaierror:

        return None


def cert_days_left(hostname):
    """Returnează zilele până la expirarea certificatului."""

    try:

        context = (
            ssl.create_default_context()
        )

        with socket.create_connection(
            (hostname, 443),
            timeout=TIMEOUT
        ) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=hostname
            ) as ssock:

                cert = (
                    ssock.getpeercert()
                )

        expires = (
            ssl.cert_time_to_seconds(
                cert["notAfter"]
            )
        )

        expiration = (
            datetime.datetime
            .fromtimestamp(
                expires,
                tz=datetime.timezone.utc
            )
        )

        now = (
            datetime.datetime.now(
                datetime.timezone.utc
            )
        )

        return (
            expiration - now
        ).days

    except Exception:

        return None


def response_times(*urls):
    """Returnează timpii de răspuns."""

    result = {}

    for url in urls:

        start = time.perf_counter()

        try:

            response = fetch(url)

            if response:

                result[url] = (
                    time.perf_counter()
                    - start
                )

            else:

                result[url] = None

        except requests.RequestException:

            result[url] = None

        time.sleep(1)

    return result


def site_report(url):
    """Colectează informațiile despre site."""

    response = fetch(url)

    if response is None:

        return {
            "status_code": None,
            "final_url": url,
            "title": "",
            "ip": None,
            "redirects": [],
            "security_score": "0/5",
            "certificate_days_left": None,
            "internal_links": 0,
            "external_links": 0,
            "disallowed_paths": []
        }

    html = response.text

    parsed = urlparse(
        response.url
    )

    domain = parsed.netloc

    links = extract_links(html)

    internal, external = split_links(
        links,
        domain
    )

    report = {

        "status_code":
            response.status_code,

        "final_url":
            response.url,

        "title":
            get_title(html),

        "ip":
            resolve(parsed.hostname),

        "redirects": [
            {
                "status_code":
                    item.status_code,
                "url":
                    item.url
            }

            for item in response.history
        ],

        "security_score":
            score_headers(
                security_headers(url)
            ),

        "certificate_days_left":
            cert_days_left(
                parsed.hostname
            ),

        "internal_links":
            len(internal),

        "external_links":
            len(external),

        "disallowed_paths":
            disallowed_paths(
                fetch_robots(url)
            )
    }

    with open(
            Path(__file__).resolve().parent / "report.json",
            "w",
            encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False
        )

    return report


if __name__ == "__main__":

    print(
        "Autotest:",
        get_status(BASE_URL)
    )