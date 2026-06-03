from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Listing])
def get_listings(
    make: str | None = Query(None),
    model: str | None = Query(None),
    year_min: int | None = Query(None),
    year_max: int | None = Query(None),
    price_min: int | None = Query(None),
    price_max: int | None = Query(None),
    mileage_max: int | None = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    db: Session = Depends(get_db),
):
    q = db.query(models.Listing)
    if make:
        q = q.filter(models.Listing.make.ilike(f"%{make}%"))
    if model:
        q = q.filter(models.Listing.model.ilike(f"%{model}%"))
    if year_min:
        q = q.filter(models.Listing.year >= year_min)
    if year_max:
        q = q.filter(models.Listing.year <= year_max)
    if price_min:
        q = q.filter(models.Listing.price >= price_min)
    if price_max:
        q = q.filter(models.Listing.price <= price_max)
    if mileage_max:
        q = q.filter(models.Listing.mileage <= mileage_max)
    return (
        q.order_by(models.Listing.deal_score.desc().nullslast())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/{listing_id}", response_model=schemas.Listing)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing
