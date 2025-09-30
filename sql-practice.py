from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

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

    activities = relationship("Activity", back_populates="user")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    strava_id = Column(Integer)
    gps_data = Column(JSON)
    date = Column(DateTime)
    type = Column(String)
    lat_long = Column(Boolean)
    processed = Column(Boolean)

    user = relationship("User", back_populates="activities")
    stations = relationship("StationsActivity", back_populates="activity")

class Stations(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Integer)
    longitude = Column(Integer)
    zone = Column(Integer)
    line = Column(String)
    network = Column(String)

    activities = relationship("StationsActivity", back_populates="station")

class StationsActivity(Base):
    __tablename__ = "stations_activity"

    id = Column(Integer, primary_key=True)
    station_name = Column(String, ForeignKey("stations.name"))
    users_id = Column(Integer, ForeignKey("activities.user_id"))

    station = relationship("Stations", back_populates="activities")
    activity = relationship("Activity", back_populates="stations")

Base.metadata.create_all(engine)

