from datetime import datetime
from pydantic import BaseModel


class ListingBase(BaseModel):
    title: str
    price: int | None = None        # CAD cents
    mileage: int | None = None      # kilometres
    year: int | None = None
    make: str | None = None
    model: str | None = None
    location: str | None = None
    source_url: str
    listing_date: datetime | None = None
    deal_score: float | None = None


class ListingCreate(ListingBase):
    pass


class Listing(ListingBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
