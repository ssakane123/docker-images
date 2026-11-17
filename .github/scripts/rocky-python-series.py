# Rocky Linux 9 の AppStream (aarch64) で提供されている最新の Python 系列を JSON で出力する。
#
#   $ python -I rocky-python-series.py
#   {"version": "3.14"}
#
# python/Dockerfile は dnf で python3.N / python3.N-pip を入れるため、
# 両方のパッケージが aarch64 (または noarch) で揃っている系列だけを候補にする。
# 出力は pin-updater --stdin にそのまま渡せる。標準ライブラリのみで動く。
import gzip
import hashlib
import io
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

REPO_URL = "https://download.rockylinux.org/pub/rocky/9/AppStream/aarch64/os/"
ARCHES = ("aarch64", "noarch")
# repodata の取得上限 (想定外に大きい応答でメモリを使い切らないため)
FETCH_LIMIT = 64 * 1024 * 1024
REPOMD_NS = "{http://linux.duke.edu/metadata/repo}"
COMMON_NS = "{http://linux.duke.edu/metadata/common}"
PACKAGE_RE = re.compile(r"python(3\.[0-9]+)(-pip)?")


def fetch(path):
    with urllib.request.urlopen(REPO_URL + path, timeout=60) as response:
        body = response.read(FETCH_LIMIT + 1)
    if len(body) > FETCH_LIMIT:
        raise ValueError("repodata is too large")
    return body


def primary_xml():
    repomd = ET.fromstring(fetch("repodata/repomd.xml"))
    (data,) = (d for d in repomd.iter(f"{REPOMD_NS}data") if d.get("type") == "primary")
    href = data.find(f"{REPOMD_NS}location").get("href")
    checksum = data.find(f"{REPOMD_NS}checksum")
    if not href.endswith(".xml.gz") or checksum.get("type") != "sha256":
        raise ValueError("unsupported repodata format")
    body = fetch(href)
    if hashlib.sha256(body).hexdigest() != checksum.text:
        raise ValueError("repodata checksum mismatch")
    return gzip.decompress(body)


def latest_series(primary):
    packages = set()
    for _, element in ET.iterparse(io.BytesIO(primary)):
        if element.tag == f"{COMMON_NS}package":
            if element.findtext(f"{COMMON_NS}arch") in ARCHES:
                packages.add(element.findtext(f"{COMMON_NS}name"))
            element.clear()
    series = {m.group(1) for name in packages
              if (m := PACKAGE_RE.fullmatch(name)) and not m.group(2)
              and f"{name}-pip" in packages}
    if not series:
        raise ValueError("no Python series found")
    return max(series, key=lambda v: tuple(map(int, v.split("."))))


if __name__ == "__main__":
    try:
        print(json.dumps({"version": latest_series(primary_xml())}))
    except Exception as error:
        print(f"ERROR: {type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(1)
