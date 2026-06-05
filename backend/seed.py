"""
Seed the database with realistic Canadian used-car listings.
Run from the backend/ directory:
    python seed.py
"""

import os
import sys
from datetime import datetime, timezone

# Allow running from repo root too
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app import models

Base.metadata.create_all(bind=engine)

LISTINGS = [
    # Toyota
    dict(title="2019 Toyota Camry XSE V6 – Clean Carfax, One Owner",
         price=2_699_000, mileage=62_000, year=2019, make="Toyota", model="Camry",
         location="Toronto, ON", source_url="https://kijiji.ca/seed/001",
         listing_date=datetime(2026, 5, 20, tzinfo=timezone.utc), deal_score=88.5),
    dict(title="2020 Toyota RAV4 AWD – Heated Seats, Lane Keep Assist",
         price=3_195_000, mileage=48_500, year=2020, make="Toyota", model="RAV4",
         location="Mississauga, ON", source_url="https://kijiji.ca/seed/002",
         listing_date=datetime(2026, 5, 28, tzinfo=timezone.utc), deal_score=82.0),
    dict(title="2018 Toyota Corolla LE – Winter Tires Included",
         price=1_749_000, mileage=91_200, year=2018, make="Toyota", model="Corolla",
         location="Ottawa, ON", source_url="https://kijiji.ca/seed/003",
         listing_date=datetime(2026, 6, 1, tzinfo=timezone.utc), deal_score=74.3),
    dict(title="2021 Toyota Highlander XLE – 3rd Row, Pano Roof",
         price=4_599_000, mileage=33_000, year=2021, make="Toyota", model="Highlander",
         location="Calgary, AB", source_url="https://kijiji.ca/seed/004",
         listing_date=datetime(2026, 5, 15, tzinfo=timezone.utc), deal_score=79.1),

    # Honda
    dict(title="2020 Honda Civic Sport – Turbo, Alloys, No Accidents",
         price=2_195_000, mileage=44_800, year=2020, make="Honda", model="Civic",
         location="Vancouver, BC", source_url="https://kijiji.ca/seed/005",
         listing_date=datetime(2026, 5, 30, tzinfo=timezone.utc), deal_score=91.2),
    dict(title="2019 Honda CR-V EX-L AWD – Sunroof, Leather",
         price=2_899_000, mileage=71_000, year=2019, make="Honda", model="CR-V",
         location="Edmonton, AB", source_url="https://kijiji.ca/seed/006",
         listing_date=datetime(2026, 5, 22, tzinfo=timezone.utc), deal_score=76.8),
    dict(title="2017 Honda Accord Touring – V6, Nav, Backup Cam",
         price=1_989_000, mileage=108_500, year=2017, make="Honda", model="Accord",
         location="Hamilton, ON", source_url="https://kijiji.ca/seed/007",
         listing_date=datetime(2026, 6, 2, tzinfo=timezone.utc), deal_score=69.5),

    # Mazda
    dict(title="2021 Mazda CX-5 GT AWD – Turbo, Bose Audio, Red Interior",
         price=3_799_000, mileage=28_000, year=2021, make="Mazda", model="CX-5",
         location="Montreal, QC", source_url="https://kijiji.ca/seed/008",
         listing_date=datetime(2026, 5, 25, tzinfo=timezone.utc), deal_score=85.6),
    dict(title="2019 Mazda3 Sport GS – Hatchback, Clean Title",
         price=1_899_000, mileage=55_300, year=2019, make="Mazda", model="Mazda3",
         location="Winnipeg, MB", source_url="https://kijiji.ca/seed/009",
         listing_date=datetime(2026, 5, 18, tzinfo=timezone.utc), deal_score=80.4),

    # Ford
    dict(title="2020 Ford F-150 XLT 4x4 – 5.0L V8, Crew Cab, Tow Pkg",
         price=4_299_000, mileage=67_000, year=2020, make="Ford", model="F-150",
         location="Saskatoon, SK", source_url="https://kijiji.ca/seed/010",
         listing_date=datetime(2026, 5, 29, tzinfo=timezone.utc), deal_score=77.3),
    dict(title="2018 Ford Escape SE AWD – Heated Seats, MyFord Touch",
         price=1_649_000, mileage=88_000, year=2018, make="Ford", model="Escape",
         location="London, ON", source_url="https://kijiji.ca/seed/011",
         listing_date=datetime(2026, 6, 3, tzinfo=timezone.utc), deal_score=65.0),

    # Hyundai / Kia
    dict(title="2022 Hyundai Tucson Preferred AWD – 14k km, Like New",
         price=3_299_000, mileage=14_200, year=2022, make="Hyundai", model="Tucson",
         location="Brampton, ON", source_url="https://kijiji.ca/seed/012",
         listing_date=datetime(2026, 6, 1, tzinfo=timezone.utc), deal_score=87.9),
    dict(title="2020 Kia Sorento EX AWD – 7 Passenger, Leather, Roof",
         price=2_999_000, mileage=52_400, year=2020, make="Kia", model="Sorento",
         location="Surrey, BC", source_url="https://kijiji.ca/seed/013",
         listing_date=datetime(2026, 5, 21, tzinfo=timezone.utc), deal_score=78.6),
    dict(title="2021 Kia Forte GT – Manual, Sport Suspension, 201hp",
         price=2_199_000, mileage=31_000, year=2021, make="Kia", model="Forte",
         location="Quebec City, QC", source_url="https://kijiji.ca/seed/014",
         listing_date=datetime(2026, 5, 26, tzinfo=timezone.utc), deal_score=83.1),

    # Subaru
    dict(title="2019 Subaru Outback 2.5i Limited – EyeSight, Nav, Leather",
         price=2_749_000, mileage=74_500, year=2019, make="Subaru", model="Outback",
         location="Victoria, BC", source_url="https://kijiji.ca/seed/015",
         listing_date=datetime(2026, 5, 17, tzinfo=timezone.utc), deal_score=72.4),
    dict(title="2020 Subaru Forester Sport – Low KM, Eyesight, Sunroof",
         price=3_099_000, mileage=39_800, year=2020, make="Subaru", model="Forester",
         location="Kelowna, BC", source_url="https://kijiji.ca/seed/016",
         listing_date=datetime(2026, 5, 31, tzinfo=timezone.utc), deal_score=81.7),

    # BMW / Mercedes (aspirational listings)
    dict(title="2018 BMW 3 Series 330i xDrive – M Sport, Pano, HUD",
         price=2_999_000, mileage=82_000, year=2018, make="BMW", model="3 Series",
         location="North York, ON", source_url="https://kijiji.ca/seed/017",
         listing_date=datetime(2026, 5, 24, tzinfo=timezone.utc), deal_score=61.2),
    dict(title="2019 Mercedes-Benz C300 4MATIC – AMG Pkg, Burmester Audio",
         price=3_499_000, mileage=69_000, year=2019, make="Mercedes-Benz", model="C300",
         location="Oakville, ON", source_url="https://kijiji.ca/seed/018",
         listing_date=datetime(2026, 5, 23, tzinfo=timezone.utc), deal_score=58.9),

    # Budget picks
    dict(title="2016 Toyota Corolla CE – Reliable, Safety Certified, Low KM",
         price=1_199_000, mileage=79_000, year=2016, make="Toyota", model="Corolla",
         location="Kitchener, ON", source_url="https://kijiji.ca/seed/019",
         listing_date=datetime(2026, 6, 2, tzinfo=timezone.utc), deal_score=70.8),
    dict(title="2017 Honda Fit LX – 56k km, Winter Tires, One Owner",
         price=1_099_000, mileage=56_000, year=2017, make="Honda", model="Fit",
         location="Halifax, NS", source_url="https://kijiji.ca/seed/020",
         listing_date=datetime(2026, 5, 27, tzinfo=timezone.utc), deal_score=84.3),
]


def seed():
    db = SessionLocal()
    inserted = 0
    skipped = 0
    try:
        for data in LISTINGS:
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
    print(f"Done — {inserted} inserted, {skipped} skipped (already existed).")


if __name__ == "__main__":
    seed()
