from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///metro_chasing.db")
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    strava_id = Column(Integer, unique=True)
    username = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    token_expires_at = Column(DateTime)

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    strava_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime)
    type = Column(String)
    gps_data = Column(JSON)
    saved_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

