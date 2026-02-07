from sqlalchemy import create_engine, Column, Integer, BigInteger, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///metro_chasing.db")
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)


class ProcessedActivity(Base):
    __tablename__ = 'processed_activities'

    id = Column(Integer, primary_key=True)
    strava_id = Column(BigInteger, unique=True, nullable=False)
    activity_name = Column(String)
    date = Column(DateTime)
    processed_at = Column(DateTime)
    activity_type = Column(String)


class StationInfo(Base):
    __tablename__ = 'station_info'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    zone = Column(String)
    network = Column(String)
    line = Column(String)

    visits = relationship('StationVisit', back_populates="station")


class StationVisit(Base):
    __tablename__ = 'station_visit'

    id = Column(Integer, primary_key=True)
    strava_id = Column(BigInteger, nullable=False)
    station_id = Column(Integer, ForeignKey("station_info.id"))

    station = relationship(StationInfo, back_populates='visits')


Base.metadata.create_all(engine)
