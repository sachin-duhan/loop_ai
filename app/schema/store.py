from app.schema.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Time

class Store(Base):
    __tablename__ = 'stores'

    store_id = Column(Integer, primary_key=True)
    timestamp_utc = Column(DateTime)
    status = Column(String)


class BusinessHours(Base):
    __tablename__ = 'business_hours'

    store_id = Column(Integer, primary_key=True)
    day = Column(Integer)
    start_time_local = Column(Time)
    end_time_local = Column(Time)


class Timezone(Base):
    __tablename__ = 'timezones'

    store_id = Column(Integer, primary_key=True)
    timezone_str = Column(String)
