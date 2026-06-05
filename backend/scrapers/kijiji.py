"""
Kijiji Autos scraper.

Usage:
    python -m scrapers.kijiji                        # Ontario, all cars, 3 pages
    python -m scrapers.kijiji --pages 10             # more pages
    python -m scrapers.kijiji --location ontario
    python -m scrapers.kijiji --location bc

Run from the backend/ directory with the venv active.
"""

import argparse
import re
import sys
import time
import os

import httpx
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app import models

LOCATIONS = {
    "ontario":  ("ontario", "l9004"),
    "bc":       ("british-columbia", "l9007"),
    "alberta":  ("alberta", "l9003"),
    "quebec":   ("quebec", "l9002"),
    "canada":   ("canada", "l0"),
}

BASE_URL = "https://www.kijiji.ca"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-CA,en;q=0.9",
}

YEAR_RE    = re.compile(r"\b(19|20)\d{2}\b")
MILEAGE_RE = re.compile(r"([\d,]+)\s*km", re.I)
PRICE_RE   = re.compile(r"\$([\d,]+)")


def _parse_price_cents(text: str) -> int | None:
    m = PRICE_RE.search(text.replace(",", ""))
    if not m:
        return None
    val = int(m.group(1).replace(",", ""))
    return val * 100 if val > 0 else None


def _parse_mileage(text: str) -> int | None:
    m = MILEAGE_RE.search(text.replace(",", ""))
    return int(m.group(1).replace(",", "")) if m else None


def _parse_year(text: str) -> int | None:
    m = YEAR_RE.search(text)
    return int(m.group(0)) if m else None


MAKE_LIST = [
    "Toyota", "Honda", "Ford", "Chevrolet", "Mazda", "Subaru", "Hyundai",
    "Kia", "Nissan", "Volkswagen", "BMW", "Mercedes-Benz", "Audi", "Dodge",
    "Jeep", "Ram", "GMC", "Cadillac", "Lexus", "Acura", "Infiniti", "Volvo",
    "Mitsubishi", "Chrysler", "Lincoln", "Buick", "Porsche", "Land Rover",
    "Mini", "Fiat", "Tesla", "Genesis", "Rivian",
]

def _parse_make_model(title: str) -> tuple[str | None, str | None]:
    """Best-effort make/model extraction from listing title."""
    for make in MAKE_LIST:
        if make.lower() in title.lower():
            # Take the token(s) after make as model
            idx = title.lower().find(make.lower())
            rest = title[idx + len(make):].strip()
            model_token = rest.split()[0] if rest.split() else None
            return make, model_token
    return None, None


def scrape_page(url: str) -> list[dict]:
    resp = httpx.get(url, headers=HEADERS, follow_redirects=True, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    cards = soup.select('[data-testid="listing-card"]')
    results = []

    for card in cards:
        try:
            # URL
            link_el = card.select_one('[data-testid="listing-link"]')
            if not link_el or not link_el.get("href"):
                continue
            href = link_el["href"]
            if href.startswith("/"):
                href = BASE_URL + href
            source_url = href.split("?")[0]

            # Title
            title_el = card.select_one('[data-testid="listing-title"]')
            title = title_el.get_text(strip=True) if title_el else link_el.get_text(strip=True)
            if not title:
                continue

            # Price
            price_el = card.select_one('[data-testid="autos-listing-price"]')
            price_cents = _parse_price_cents(price_el.get_text() if price_el else "")

            # Location
            loc_el = card.select_one('[data-testid="listing-location"]')
            location = loc_el.get_text(strip=True) if loc_el else None

            # Mileage — check description text
            desc_el = card.select_one('[data-testid="listing-description"]')
            card_text = card.get_text()
            mileage = _parse_mileage(card_text)

            # Year from title
            year = _parse_year(title)

            # Make / model from title
            make, model = _parse_make_model(title)

            results.append(dict(
                title=title,
                price=price_cents,
                mileage=mileage,
                year=year,
                make=make,
                model=model,
                location=location,
                source_url=source_url,
            ))
        except Exception as e:
            print(f"  [warn] skipped a card: {e}")

    # Next page URL
    next_el = soup.select_one('a[title="Next"]') or soup.select_one('[data-testid="pagination-next-link"]')
    next_url = None
    if next_el and next_el.get("href"):
        href = next_el["href"]
        next_url = (BASE_URL + href) if href.startswith("/") else href

    return results, next_url


def save_listings(listings: list[dict]) -> tuple[int, int]:
    db = SessionLocal()
    inserted = skipped = 0
    try:
        for data in listings:
            exists = db.query(models.Listing).filter(
                models.Listing.source_url == data["source_url"]
            ).first()
            if exists:
                skipped += 1
                continue
            db.add(models.Listing(**data))
            inserted += 1
        db.commit()
    finally:
        db.close()
    return inserted, skipped


def run(location: str = "ontario", max_pages: int = 3):
    loc_name, loc_code = LOCATIONS.get(location, LOCATIONS["ontario"])
    start_url = f"{BASE_URL}/b-cars-trucks/{loc_name}/c174{loc_code}"

    print(f"Scraping Kijiji Autos — {location}, up to {max_pages} pages")
    print(f"Starting URL: {start_url}\n")

    url = start_url
    total_inserted = total_skipped = 0

    for page_num in range(1, max_pages + 1):
        print(f"Page {page_num}: {url}")
        try:
            listings, next_url = scrape_page(url)
        except httpx.HTTPStatusError as e:
            print(f"  HTTP error {e.response.status_code}, stopping.")
            break

        inserted, skipped = save_listings(listings)
        total_inserted += inserted
        total_skipped += skipped
        print(f"  Found {len(listings)} listings → {inserted} new, {skipped} already in DB")

        if not next_url:
            print("  No next page found, done.")
            break

        url = next_url
        if page_num < max_pages:
            time.sleep(1.5)  # polite delay

    print(f"\nDone — {total_inserted} inserted, {total_skipped} skipped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Kijiji Autos listings")
    parser.add_argument("--location", default="ontario", choices=list(LOCATIONS.keys()))
    parser.add_argument("--pages", type=int, default=3)
    args = parser.parse_args()
    run(location=args.location, max_pages=args.pages)
