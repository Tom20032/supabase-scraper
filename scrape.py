

import requests
import pandas as pd
from bs4 import BeautifulSoup
from supabase import create_client
from datetime import datetime

# -----------------------------
# Supabase setup
# -----------------------------
SUPABASE_URL = "https://lgsppysypeaefpqaiyal.supabase.co"
SUPABASE_KEY = "sb_publishable_DFEPfhkigL_5ddZqUwQrMw_49uLbnxH"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
scrape_time = datetime.now().isoformat()

# -----------------------------
# Scraper
# -----------------------------
url = "https://nl.wikipedia.org/wiki/Lijst_van_bestverkochte_albums_wereldwijd"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")

table = soup.select_one("table.wikitable")

rows = []

for tr in table.select("tbody tr")[1:21]:  # top 20
    tds = tr.select("td")
    if len(tds) < 5:
        continue

    artiest = tds[0].get_text(strip=True)
    album = tds[1].get_text(strip=True)
    jaar = tds[2].get_text(strip=True)
    genre = tds[3].get_text(strip=True)
    verkocht = tds[4].get_text(strip=True)

    rows.append({
        "artiest": artiest,
        "album": album,
        "jaar": jaar,
        "genre": genre,
        "verkocht": verkocht,
        "scraped_at": scrape_time,
    })

df = pd.DataFrame(rows)
print(df)

# -----------------------------
# Supabase insert
# -----------------------------
result = supabase.table("albums").insert(rows).execute()

print(f"✅ Inserted {len(rows)} rows into Supabase")
