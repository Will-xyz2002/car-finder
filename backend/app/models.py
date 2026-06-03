from datetime import datetime
from sqlalchemy import Column, Float, Integer, String, DateTime, Text
from app.database import Base


class Listing(Base):
    __tablename__ = "listings"

    id           = Column(Integer, primary_key=True, index=True)
    title        = Column(Text, nullable=False)
    price        = Column(Integer)    # CAD cents
    mileage      = Column(Integer)    # kilometres
    year         = Column(Integer)
    make         = Column(String(100))
    model        = Column(String(100))
    location     = Column(Text)
    source_url   = Column(Text, unique=True, nullable=False)
    listing_date = Column(DateTime(timezone=True))
    deal_score   = Column(Float)      # 0-100, higher is better
    created_at   = Column(DateTime(timezone=True), default=datetime.utcnow)
