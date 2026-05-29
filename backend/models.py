from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from db import Base


class Listing(Base):
    __tablename__ = "listings"
    __table_args__ = (UniqueConstraint("source", "source_id"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    source: Mapped[str] = mapped_column(String, nullable=False)
    source_id: Mapped[str] = mapped_column(String, nullable=False)
    source_url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price_chf: Mapped[int] = mapped_column(Integer, nullable=False)
    rooms: Mapped[float] = mapped_column(Float, nullable=False)
    area_m2: Mapped[int | None] = mapped_column(Integer, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=False)
    zip_code: Mapped[str | None] = mapped_column(String, nullable=True)
    kreis: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_furnished: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    gender_preference: Mapped[str | None] = mapped_column(String, nullable=True)
    min_stay_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_stay_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    available_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    available_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_sublet: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    images: Mapped[str] = mapped_column(String, nullable=False, default="[]")
    first_seen: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_summer_sublet: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class CommuteCache(Base):
    __tablename__ = "commute_cache"
    __table_args__ = (UniqueConstraint("origin_lat", "origin_lng", "dest_lat", "dest_lng", "mode"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    origin_lat: Mapped[float] = mapped_column(Float, nullable=False)
    origin_lng: Mapped[float] = mapped_column(Float, nullable=False)
    dest_lat: Mapped[float] = mapped_column(Float, nullable=False)
    dest_lng: Mapped[float] = mapped_column(Float, nullable=False)
    mode: Mapped[str] = mapped_column(String, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)