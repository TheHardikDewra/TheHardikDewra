#!/usr/bin/env python3
"""Check every link in README.md still resolves. Exits 1 if any are dead."""
import re, sys, json, pathlib
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Hosts that block automated requests but are fine in a browser.
BOT_WALLED = ("linkedin.com", "medium.com", "x.com", "twitter.com", "instagram.com")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " \
     "(KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"

def check(url):
    if any(h in url for h in BOT_WALLED):
        return url, "skipped", "bot-walled, verify by hand"
    for attempt in range(3):
        try:
            req = Request(url, headers={"User-Agent": UA})
            with urlopen(req, timeout=30) as r:
                return url, r.status, ""
        except HTTPError as e:
            if e.code in (403, 429) and attempt < 2:
                continue
            return url, e.code, e.reason
        except (URLError, OSError) as e:
            if attempt < 2:
                continue
            return url, "ERR", str(e)[:80]
    return url, "ERR", "exhausted retries"

def main():
    readme = pathlib.Path(__file__).resolve().parent.parent / "README.md"
    urls = sorted(set(re.findall(r'https?://[^\s)"\'<>]+', readme.read_text(encoding="utf-8"))))
    urls = [u.rstrip('.,);') for u in urls]
    print(f"Checking {len(urls)} links from README.md\n")

    with ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(check, urls))

    dead = [(u, s, m) for u, s, m in results if s not in (200, "skipped")]
    ok = sum(1 for _, s, _ in results if s == 200)
    skipped = sum(1 for _, s, _ in results if s == "skipped")

    for u, s, m in results:
        if s not in (200, "skipped"):
            print(f"DEAD  {s:>6}  {u}  {m}")
    print(f"\n{ok} ok, {skipped} skipped, {len(dead)} dead")

    if dead:
        body = "These links in the profile README no longer resolve:\n\n"
        body += "\n".join(f"- `{s}` {u} {m}".rstrip() for u, s, m in dead)
        body += "\n\nThe page claims every link is live, so fix or remove them."
        pathlib.Path("dead-links.md").write_text(body, encoding="utf-8")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
