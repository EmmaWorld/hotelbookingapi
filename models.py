from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#--------------------------------------------------------------

Base = declarative_base()
booking_user = Table(
    'booking_user',
    Base.metadata,
    Column('bookings_id', Integer, ForeignKey('bookings.id'), primary_key=True)
)
# Customer Model
class Customer(Base):
    __tablename__ = 'Customer'
    CustomerID = Column(Integer, primary_key=True)
    Name = Column(String)
    Email = Column(String)
    Phone = Column(Integer)
    Address = Column(String)

# Hotel Model
class Hotel(Base):
    __tablename__ = 'Hotel'
    HotelID = Column(Integer, primary_key=True)
    Name = Column(String)
    Address = Column(String)
    Phone = Column(String)
    Email = Column(String)
    Rating = Column(Integer)
    Capacity = Column(Integer)

# HotelBooking Model
class HotelBooking(Base):
    __tablename__ = 'HotelBooking'
    BookingID = Column(Integer, primary_key=True)
    CustomerID = Column(Integer, ForeignKey('Customer.CustomerID'))
    HotelID = Column(Integer, ForeignKey('Hotel.HotelID'))
    CheckInDate = Column(Date)
    CheckOutDate = Column(Date)
    RoomType = Column(String)
    TotalPrice = Column(Float)

    customer = relationship("Customer", secondary='booking_user', back_populates='hotelbookings')
    hotel = relationship("Hotel", backref="bookings")


def create_database():
    engine = create_engine('sqlite:///hotel_management.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# Usage:
session = create_database()