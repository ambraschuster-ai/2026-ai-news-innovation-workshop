"""
Archive documented.info (IRC Signpost / Zendesk Guide) before it disappears.

The site is unmaintained as of June 30, 2026 ("no longer being updated,
our chat is no longer monitored"). It holds the only structured provider
dataset in Documented's orbit. This grabs everything, in every locale,
as raw JSON.

Stdlib only, on purpose: this needs to run anywhere, today, with no setup.

    python3 ingest/zendesk.py
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://signpost-nyc.zendesk.com/api/v2/help_center"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "archives", "documented_info")
UA = "Documented-Archive/1.0 (newsroom research; tkc.intern1@journalism.cuny.edu)"

# Zendesk Guide caps per_page at 100.
PER_PAGE = 100


def get(url, tries=4):
    """GET with backoff. Returns parsed JSON, or None on a hard 404."""
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                wait = int(e.headers.get("Retry-After", 2 ** (attempt + 1)))
                print(f"    {e.code}, retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < tries - 1:
                time.sleep(2 ** (attempt + 1))
                continue
            raise
    return None


def paginate(path, key):
    """Walk a Zendesk collection endpoint, yielding records from `key`."""
    url = f"{BASE}/{path}?per_page={PER_PAGE}"
    seen = 0
    while url:
        data = get(url)
        if not data:
            break
        batch = data.get(key, [])
        seen += len(batch)
        for rec in batch:
            yield rec
        url = data.get("next_page")
        if url:
            time.sleep(0.4)  # be polite to a server nobody is maintaining
    print(f"    {path} -> {seen} records")


def dump(name, obj):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    size = os.path.getsize(path)
    print(f"  wrote {name}.json  ({len(obj)} records, {size:,} bytes)")
    return len(obj)


def main():
    print("Archiving documented.info (Zendesk Guide / IRC Signpost)\n")

    locales = get(f"{BASE}/locales.json") or {}
    loc_list = locales.get("locales", ["en-us"])
    print(f"Locales: {', '.join(loc_list)}\n")
    dump("_locales", loc_list)

    manifest = {"locales": loc_list, "counts": {}}

    # Articles are locale-scoped; categories/sections carry the taxonomy.
    for loc in loc_list:
        print(f"[{loc}]")
        for path, key in (
            (f"{loc}/articles.json", "articles"),
            (f"{loc}/categories.json", "categories"),
            (f"{loc}/sections.json", "sections"),
        ):
            recs = list(paginate(path, key))
            n = dump(f"{key}__{loc}", recs)
            manifest["counts"][f"{key}.{loc}"] = n
        print()

    dump("_manifest", manifest)
    print("Done. Raw JSON in data/archives/documented_info/")
    print("\nNOTE: the 358-provider service map is a separate datastore rendered")
    print("client-side on documented.info. Run ingest/service_map.py for that.")


if __name__ == "__main__":
    main()
