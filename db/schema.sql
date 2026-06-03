CREATE TABLE IF NOT EXISTS listings (
    id            SERIAL PRIMARY KEY,
    title         TEXT NOT NULL,
    price         INTEGER,           -- CAD cents
    mileage       INTEGER,           -- kilometres
    year          INTEGER,
    make          VARCHAR(100),
    model         VARCHAR(100),
    location      TEXT,
    source_url    TEXT UNIQUE NOT NULL,
    listing_date  TIMESTAMPTZ,
    deal_score    FLOAT,             -- 0-100, higher is better
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_listings_make        ON listings(make);
CREATE INDEX IF NOT EXISTS idx_listings_model       ON listings(model);
CREATE INDEX IF NOT EXISTS idx_listings_year        ON listings(year);
CREATE INDEX IF NOT EXISTS idx_listings_price       ON listings(price);
CREATE INDEX IF NOT EXISTS idx_listings_deal_score  ON listings(deal_score DESC NULLS LAST);
