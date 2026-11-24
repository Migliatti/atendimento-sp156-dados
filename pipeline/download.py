"""Step 1: download the public CSV (skipped if the file is already there)."""
import shutil
import urllib.request

from .config import DOWNLOAD_URL, RAW_FILE


def download(force: bool = False):
    if RAW_FILE.exists() and not force:
        print(f"[download] already there: {RAW_FILE}")
        return RAW_FILE
    RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = RAW_FILE.with_suffix(".part")
    print(f"[download] {DOWNLOAD_URL}")
    req = urllib.request.Request(DOWNLOAD_URL, headers={"User-Agent": "sp156-study-project"})
    with urllib.request.urlopen(req, timeout=120) as resp, open(tmp, "wb") as out:
        shutil.copyfileobj(resp, out)
    tmp.rename(RAW_FILE)
    print(f"[download] saved {RAW_FILE.stat().st_size / 1e6:.0f} MB")
    return RAW_FILE
