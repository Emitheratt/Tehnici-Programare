
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

import time
import requests
import urllib.request
import urllib.error
import re
import hashlib
import json
import socket
import ssl
import datetime

from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser


# ============================================================
# FUNCȚIE AJUTĂTOARE
# ============================================================

def safe_get(url, timeout=TIMEOUT, **kwargs):
    """
    Face o cerere GET folosind requests.
    În cazul unei erori, returnează None.
    """
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0"},
            **kwargs
        )
        return response
    except requests.RequestException as e:
        print("Eroare la accesarea", url, ":", e)
        return None


# ============================================================
# PARTEA 1 – IMPORTURI
# EXERCIȚIILE 1–8

print("\n" + "=" * 60)
print("PARTEA 1 – IMPORTURI")
print("=" * 60)


# Exercițiul 1

import requests

print("\nEx. 1 - requests version:", requests.__version__)

import urllib.request

# requests este bibliotecă externă.
# urllib.request face parte din biblioteca standard Python.


# Exercițiul 2

response = safe_get(BASE_URL)

if response is not None:
    print("Ex. 2 - status:", response.status_code)
else:
    print("Ex. 2 - cererea nu a putut fi efectuată")


from requests import get

try:
    response2 = get(
        BASE_URL,
        timeout=TIMEOUT,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    print(
        "Ex. 2 - status (from requests import get):",
        response2.status_code
    )
except requests.RequestException as e:
    print("Ex. 2 - eroare:", e)


# Exercițiul 3

import requests as rq

response = safe_get(BASE_URL)

if response is not None:
    print("Ex. 3 - status:", response.status_code)
else:
    print("Ex. 3 - cererea nu a putut fi efectuată")


# Exercițiul 4

print("\nEx. 4 - test urllib.request")

try:
    request = urllib.request.Request(
        BASE_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(
        request,
        timeout=TIMEOUT
    ) as response:
        body = response.read().decode("utf-8", errors="replace")

        print("Ex. 4 - status:", response.status)
        print(body[:200])

except urllib.error.HTTPError as e:
    print("Ex. 4 - serverul a returnat HTTP", e.code)

    # Fallback cu requests pentru ca exercițiul să continue
    fallback = safe_get(BASE_URL)

    if fallback is not None:
        print(
            "Ex. 4 - fallback requests status:",
            fallback.status_code
        )
        print(fallback.text[:200])

except urllib.error.URLError as e:
    print("Ex. 4 - eroare URL:", e)

except Exception as e:
    print("Ex. 4 - eroare:", e)


# Exercițiul 5

print("\nEx. 5 - dir(requests):")

names = dir(requests)

print(names)


# Exercițiul 6

print("\nEx. 6 - help(requests.get):")

help(requests.get)

response = safe_get(BASE_URL)

if response is not None:
    print("Ex. 6 - status:", response.status_code)
else:
    print("Ex. 6 - cererea nu a reușit")


# Exercițiul 7

start = time.perf_counter()

response = safe_get(BASE_URL)

end = time.perf_counter()

print(
    "Ex. 7 - perf_counter:",
    end - start,
    "secunde"
)

if response is not None:
    print(
        "Ex. 7 - response.elapsed:",
        response.elapsed.total_seconds(),
        "secunde"
    )
else:
    print("Ex. 7 - nu există response.elapsed")


# Exercițiul 8

print("\nEx. 8 - verificare BeautifulSoup")

try:
    import bs4

    print(
        "Ex. 8 - bs4 este instalat.",
        bs4.__version__
    )

except ImportError:
    print(
        "Ex. 8 - bs4 nu este instalat."
    )
    print(
        "Instalați cu: python -m pip install beautifulsoup4"
    )


# ============================================================
# PARTEA 2 – METODE ȘI ATRIBUTE
# EXERCIȚIILE 9–20

print("\n" + "=" * 60)
print("PARTEA 2 – METODE ȘI ATRIBUTE")
print("=" * 60)


# Exercițiul 9

response = safe_get(BASE_URL)

if response is not None:

    print(
        "Ex. 9 - status_code:",
        response.status_code
    )

    print(
        "Ex. 9 - ok:",
        response.ok
    )

    print(
        "Ex. 9 - url:",
        response.url
    )

    print(
        "Ex. 9 - encoding:",
        response.encoding
    )

else:
    print("Ex. 9 - fără răspuns")


# Exercițiul 10

print("\nEx. 10 - raise_for_status")

try:

    if response is not None:
        response.raise_for_status()
        print("Ex. 10 - cererea principală este OK")

    bad = safe_get(
        BASE_URL + "/this-page-does-not-exist"
    )

    if bad is not None:

        try:
            bad.raise_for_status()

        except requests.HTTPError:

            print(
                "Ex. 10 - pagina nu există "
                "sau serverul a returnat o eroare HTTP."
            )

except requests.RequestException as e:

    print("Ex. 10 - eroare:", e)


# Exercițiul 11

response = safe_get(BASE_URL)

if response is not None:

    print("\nEx. 11 - headers:")

    for name, value in response.headers.items():

        print(
            f"{name}: {value}"
        )

else:

    print("Ex. 11 - fără răspuns")


# Exercițiul 12

if response is not None:

    print(
        "Ex. 12 - Server:",
        response.headers.get(
            "Server",
            "lipsește"
        )
    )

    print(
        "Ex. 12 - Content-Type:",
        response.headers.get(
            "Content-Type",
            "lipsește"
        )
    )

    print(
        "Ex. 12 - content-type:",
        response.headers.get(
            "content-type",
            "lipsește"
        )
    )


# Exercițiul 13


if response is not None:

    count = response.text.lower().count(
        "cyber"
    )

    print(
        "Ex. 13 - cyber apare de",
        count,
        "ori."
    )


# Exercițiul 14

if response is not None:

    html = response.text

    start = html.find("<title>")

    if start != -1:

        start += len("<title>")

        end = html.find(
            "</title>",
            start
        )

        if end != -1:

            title = html[
                start:end
            ].strip()

        else:

            title = ""

    else:

        title = ""

    print(
        "Ex. 14 - titlu:",
        title
    )


# Exercițiul 15

if response is not None:

    lines = response.text.splitlines()

    longest = (
        max(lines, key=len)
        if lines
        else ""
    )

    print(
        "Ex. 15 - număr linii:",
        len(lines)
    )

    print(
        "Ex. 15 - lungimea celei mai lungi linii:",
        len(longest)
    )


# Exercițiul 16

if response is not None:

    if response.url.startswith(
        "https://"
    ):

        print(
            "Ex. 16 - Conexiune securizată"
        )

    else:

        print(
            "Ex. 16 - Conexiune nesecurizată"
        )


# Exercițiul 17

print("\nEx. 17 - redirecționări")

response = safe_get(
    "http://cybercor.org"
)

if response is not None:

    for item in response.history:

        print(
            "Ex. 17 - redirecționare:",
            item.status_code,
            item.url
        )

    print(
        "Ex. 17 - URL final:",
        response.url
    )

else:

    print("Ex. 17 - cererea nu a reușit")


# Exercițiul 18

head_response = None
get_response = None

try:

    head_response = requests.head(
        BASE_URL,
        timeout=TIMEOUT,
        headers={"User-Agent": "Mozilla/5.0"}
    )

except requests.RequestException as e:

    print("Ex. 18 - HEAD eroare:", e)


try:

    get_response = requests.get(
        BASE_URL,
        timeout=TIMEOUT,
        headers={"User-Agent": "Mozilla/5.0"}
    )

except requests.RequestException as e:

    print("Ex. 18 - GET eroare:", e)


print(
    "Ex. 18 - HEAD bytes:",
    len(head_response.content)
    if head_response is not None
    else 0
)

print(
    "Ex. 18 - GET bytes:",
    len(get_response.content)
    if get_response is not None
    else 0
)


# Exercițiul 19

response = safe_get(BASE_URL)

if response is not None:

    if response.cookies:

        for cookie in response.cookies:

            print(
                "Ex. 19 -",
                cookie.name,
                cookie.secure
            )

    else:

        print(
            "Ex. 19 - Niciun cookie setat."
        )


# Exercițiul 20

session = requests.Session()

session.headers.update({
    "User-Agent": "WebLab-Emilia"
})

try:

    echo = session.get(
        ECHO_URL + "/headers",
        timeout=TIMEOUT
    )

    print(
        "Ex. 20 - User-Agent trimis:",
        echo.json()
        .get("headers", {})
        .get("User-Agent")
    )

except requests.RequestException as e:

    print(
        "Ex. 20 - eroare:",
        e
    )


# ============================================================
# PARTEA 3 – FUNCȚII PROPRII
# EXERCIȚIILE 21–34

print("\n" + "=" * 60)
print("PARTEA 3 – FUNCȚII PROPRII")
print("=" * 60)


# Exercițiul 21

def fetch(url):
    """Returnează obiectul răspuns."""

    return safe_get(url)


result = fetch(BASE_URL)

print(
    "Ex. 21 -",
    result.status_code
    if result is not None
    else "eroare"
)


# Exercițiul 22

def get_status(url):
    """Returnează codul HTTP."""

    response = safe_get(url)

    if response is None:
        return None

    return response.status_code


for path in [
    "/",
    "/robots.txt",
    "/sitemap.xml"
]:

    print(
        "Ex. 22 -",
        path,
        get_status(BASE_URL + path)
    )

    time.sleep(1)


# Exercițiul 23

def fetch(url, timeout=10):
    """Descarcă URL-ul."""

    return safe_get(
        url,
        timeout=timeout
    )


result = fetch(BASE_URL)

print(
    "Ex. 23 - implicit:",
    result.status_code
    if result
    else "eroare"
)

result = fetch(
    BASE_URL,
    timeout=3
)

print(
    "Ex. 23 - timeout=3:",
    result.status_code
    if result
    else "eroare"
)


# Exercițiul 24

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


response = fetch(BASE_URL)

if response:

    print(
        "Ex. 24 -",
        get_title(response.text)
    )


# Exercițiul 25

print(
    "Ex. 25 - docstring:"
)

help(get_title)


# Exercițiul 26

def get_status_typed(
    url: str
) -> int:

    response = safe_get(url)

    if response is None:
        return 0

    return response.status_code


print(
    "Ex. 26 -",
    get_status_typed(BASE_URL)
)

print(
    "Type hints documentează tipurile."
)


# Exercițiul 27

def page_exists(
    url: str
) -> bool:

    response = safe_get(url)

    if response is None:
        return False

    try:

        response.raise_for_status()

        return True

    except requests.RequestException:

        return False


print(
    "Ex. 27 - cybercor:",
    page_exists(BASE_URL)
)

print(
    "Ex. 27 - domeniu invalid:",
    page_exists(
        "https://this-domain-does-not-exist.invalid"
    )
)


# Exercițiul 28

def check_paths(
    base,
    paths
):

    result = {}

    for path in paths:

        try:

            response = safe_get(
                base + path
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


print(
    "Ex. 28 -",
    check_paths(
        BASE_URL,
        [
            "/",
            "/robots.txt",
            "/sitemap.xml"
        ]
    )
)


# Exercițiul 29

def get_header(
    url,
    name,
    default="lipsește"
):

    response = safe_get(url)

    if response is None:
        return default

    return response.headers.get(
        name,
        default
    )


print(
    "Ex. 29 - Server:",
    get_header(
        BASE_URL,
        "Server"
    )
)


# Exercițiul 30

SECURITY_HEADERS = [

    "Strict-Transport-Security",

    "Content-Security-Policy",

    "X-Frame-Options",

    "X-Content-Type-Options",

    "Referrer-Policy"

]


def security_headers(url):

    response = safe_get(url)

    if response is None:

        return {
            name: False
            for name in SECURITY_HEADERS
        }

    return {
        name: name in response.headers
        for name in SECURITY_HEADERS
    }


print(
    "Ex. 30 -",
    security_headers(BASE_URL)
)


# Exercițiul 31

def score_headers(results):

    score = sum(
        results.values()
    )

    return (
        f"{score}/{len(results)}"
    )


print(
    "Ex. 31 -",
    score_headers(
        security_headers(BASE_URL)
    )
)


# Exercițiul 32

def fetch_robots(base):
    try:
        response = safe_get(
            base.rstrip("/") +
            "/robots.txt"
        )
        if response is None:
            return None

        if response.status_code == 404:
            return None

        response.raise_for_status()

        return response.text

    except requests.RequestException:
        return None

def disallowed_paths(
    robots_text
):

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

robots = fetch_robots(BASE_URL)
print(
    "Ex. 32 -",
    disallowed_paths(robots)
)


# Exercițiul 33

def response_times(*urls):

    result = {}

    for url in urls:

        start = time.perf_counter()

        try:

            response = safe_get(url)

            if response is not None:

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


print(
    "Ex. 33 -",
    response_times(
        BASE_URL,
        BASE_URL + "/robots.txt"
    )
)


# Exercițiul 34

def log(
    message,
    **details
):

    text = message

    for key, value in details.items():

        text += (
            f" | {key}={value}"
        )

    print(text)


log(
    "verificat",
    url=BASE_URL,
    status=200
)


# ============================================================
# PARTEA 4 – MODULE STANDARD
# EXERCIȚIILE 35–43

print("\n" + "=" * 60)
print("PARTEA 4 – MODULE STANDARD")
print("=" * 60)


# Exercițiul 35

parsed = urlparse(
    "https://cybercor.org/path?x=1#top"
)

print(
    "Ex. 35 - scheme:",
    parsed.scheme
)

print(
    "Ex. 35 - netloc:",
    parsed.netloc
)

print(
    "Ex. 35 - path:",
    parsed.path
)

print(
    "Ex. 35 - query:",
    parsed.query
)

print(
    "Ex. 35 - fragment:",
    parsed.fragment
)


# Exercițiul 36

for relative in [
    "/about",
    "contact.html",
    "../index.html"
]:

    print(
        "Ex. 36 -",
        relative,
        "->",
        urljoin(
            BASE_URL,
            relative
        )
    )


# Exercițiul 37

def extract_links(html):

    links = re.findall(
        r'href=["\']([^"\']+)["\']',
        html
    )

    return list(
        dict.fromkeys(links)
    )


response = safe_get(BASE_URL)

if response:

    links = extract_links(
        response.text
    )

    print(
        "Ex. 37 - linkuri:",
        links
    )

else:

    links = []

    print(
        "Ex. 37 - nu s-a putut accesa pagina"
    )


# Exercițiul 38

def split_links(
    links,
    domain
):

    internal = []

    external = []

    for link in links:

        full = urljoin(
            BASE_URL,
            link
        )

        netloc = urlparse(
            full
        ).netloc

        if netloc == domain:

            internal.append(link)

        else:

            external.append(link)

    return internal, external


internal, external = split_links(
    links,
    urlparse(BASE_URL).netloc
)

print(
    "Ex. 38 - interne:",
    internal
)

print(
    "Ex. 38 - externe:",
    external
)


# Exercițiul 39

class ImageFinder(
    HTMLParser
):

    def __init__(self):

        super().__init__()

        self.images = []


    def handle_starttag(
        self,
        tag,
        attrs
    ):

        if tag.lower() == "img":

            src = dict(
                attrs
            ).get("src")

            if src:

                self.images.append(
                    src
                )


test_html = """
<html>
<body>
<img src="/logo.png" alt="Logo">
<IMG SRC="poza.jpg">
<img alt="imagine fără src">
<img src="https://cdn.example.com/banner.webp">
<a href="/despre">Aceasta nu este o imagine</a>
</body>
</html>
"""


finder = ImageFinder()

finder.feed(
    test_html
)

print(
    "Ex. 39 - test:",
    finder.images
)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp"
]

print(
    "Ex. 39 - Testul a trecut!"
)


response = safe_get(BASE_URL)

if response:

    finder = ImageFinder()

    finder.feed(
        response.text
    )

    print(
        "Ex. 39 -",
        len(finder.images),
        "imagini găsite"
    )

    for src in finder.images:

        print(src)


# Exercițiul 40

def page_fingerprint(url):

    response = safe_get(url)

    if response is None:
        return None

    return hashlib.sha256(
        response.content
    ).hexdigest()


fp1 = page_fingerprint(
    BASE_URL
)

fp2 = page_fingerprint(
    BASE_URL
)

print(
    "Ex. 40 - identice:",
    fp1 == fp2
)


# Exercițiul 41

response = safe_get(BASE_URL)

headers_file = "headers.json"

if response:

    with open(
        headers_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            dict(response.headers),
            file,
            indent=2
        )


    with open(
        headers_file,
        "r",
        encoding="utf-8"
    ) as file:

        loaded_headers = json.load(
            file
        )


    print(
        "Ex. 41 - Server:",
        loaded_headers.get(
            "Server",
            "lipsește"
        )
    )

else:

    print(
        "Ex. 41 - nu există response"
    )


# Exercițiul 42

def resolve(hostname):

    try:

        return socket.gethostbyname(
            hostname
        )

    except socket.gaierror:

        return None


ip = resolve(
    "cybercor.org"
)

print(
    "Ex. 42 - IP:",
    ip
)


# Exercițiul 43

def cert_days_left(
    hostname
):

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

    except Exception as e:

        print(
            "Ex. 43 - certificatul "
            "nu a putut fi verificat:",
            e
        )

        return None


days = cert_days_left(
    "cybercor.org"
)

print(
    "Ex. 43 - zile certificat:",
    days
)


print("\n" + "=" * 60)
print("EXERCIȚIILE 1–43 S-AU TERMINAT")
print("=" * 60)