from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import create_database, Customer, HotelBooking, Hotel
from typing import List
from datetime import datetime
app = FastAPI()

# Create database session
session = create_database()

# Define request/response models
class CustomerRequest(BaseModel):
    name: str
    email: str
    phone: int
    address: str

class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    email: str
    phone: int
    address: str
    
    
    class Config:
        orm_mode = True
    
# Define request/response models
class HotelRequest(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    rating: int
    capacity: int

class HotelResponse(BaseModel):
    hotel_id: int
    name: str
    address: str
    phone: str
    email: str
    rating: int
    capacity: int

class HotelBookingRequest(BaseModel):
    customer_id: int
    hotel_id: int
    check_in_date: str
    check_out_date: str
    room_type: str
    total_price: float

class HotelBookingResponse(BaseModel):
    booking_id: int
    customer_id: int
    hotel_id: int
    check_in_date: str
    check_out_date: str
    room_type: str
    total_price: float

# Define request/response models
class CustomerPatchRequest(BaseModel):
    name: str = None
    email: str = None
    phone: str = None
    address: str = None

class HotelBookingPatchRequest(BaseModel):
    check_in_date: str = None
    check_out_date: str = None
    room_type: str = None
    total_price: float = None

# Define request/response models
class HotelPatchRequest(BaseModel):
    name: str = None
    address: str = None
    phone: str = None
    email: str = None
    rating: int = None
    capacity: int = None
    


# GET request to retrieve all customers
@app.get("/")
def get_all_customers() :
    all_customers = session.query(Customer).all()
    return all_customers



# Routes for Customer entity
@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    customer = session.query(Customer).filter(Customer.CustomerID == customer_id).first()
    if customer:
        return CustomerResponse(
            customer_id=customer.CustomerID,
            name=customer.Name,
            email=customer.Email,
            phone=customer.Phone,
            address=customer.Address
        )
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

@app.post("/customers")
def create_customer(customer: CustomerRequest):
    new_customer = Customer(
        Name=customer.name,
        Email=customer.email,
        Phone=customer.phone,
        Address=customer.address
    )
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return CustomerResponse(
        customer_id=new_customer.CustomerID,
        name=new_customer.Name,
        email=new_customer.Email,
        phone=new_customer.Phone,
        address=new_customer.Address
    )
   
    
@app.patch("/customers/{customer_id}")
def patch_customer(customer_id: int, patch_data: CustomerPatchRequest):
    customer = session.query(Customer).filter(Customer.CustomerID == customer_id).first()
    if customer:
        # Update the customer with the provided patch data
        if patch_data.name:
            customer.Name = patch_data.name
        if patch_data.email:
            customer.Email = patch_data.email
        if patch_data.phone:
            customer.Phone = patch_data.phone
        if patch_data.address:
            customer.Address = patch_data.address

        session.commit()

        return {"message": "Customer updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    customer = session.query(Customer).filter(Customer.CustomerID == customer_id).first()
    if customer:
        session.delete(customer)
        session.commit()
        return {"message": "Customer deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


# Routes for HotelBooking entity

@app.get("/bookings")
def get_all_booking() :
    all_booking = session.query(HotelBooking).all()
    return all_booking


@app.get("/bookings/{booking_id}")
def get_booking(booking_id: int):
    booking = session.query(HotelBooking).filter(HotelBooking.BookingID == booking_id).first()
    if booking:
        return HotelBookingResponse(
            booking_id=booking.BookingID,
            customer_id=booking.CustomerID,
            hotel_id=booking.HotelID,
            check_in_date=str(booking.CheckInDate),
            check_out_date=str(booking.CheckOutDate),
            room_type=booking.RoomType,
            total_price=booking.TotalPrice
        )
    else:
        raise HTTPException(status_code=404, detail="Booking not found")

@app.post("/bookings")
def create_booking(booking: HotelBookingRequest):
    format_string = "%Y/%m/%d"
    new_booking = HotelBooking(
        CustomerID=booking.customer_id,
        HotelID=booking.hotel_id,
        CheckInDate=datetime.strptime(booking.check_in_date, format_string).date(),
        CheckOutDate=datetime.strptime(booking.check_out_date, format_string).date(),
        RoomType=booking.room_type,
        TotalPrice=booking.total_price
    )
    session.add(new_booking)
    session.commit()
    session.refresh(new_booking)
    return HotelBookingResponse(
        booking_id=new_booking.BookingID,
        customer_id=new_booking.CustomerID,
        hotel_id=new_booking.HotelID,
        check_in_date=str(new_booking.CheckInDate),
        check_out_date=str(new_booking.CheckOutDate),
        room_type=new_booking.RoomType,
        total_price=new_booking.TotalPrice
    )
    

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int):
    booking = session.query(HotelBooking).filter(HotelBooking.BookingID == booking_id).first()
    if booking:
        session.delete(booking)
        session.commit()
        return {"message": "Booking deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="booking not found")
    
@app.patch("/bookings/{booking_id}")
def patch_booking(booking_id: int, patch_data: HotelBookingPatchRequest):
    booking = session.query(HotelBooking).filter(HotelBooking.BookingID == booking_id).first()
    if booking:
        # Update the booking with the provided patch data
        if patch_data.check_in_date:
            booking.CheckInDate = patch_data.check_in_date
        if patch_data.check_out_date:
            booking.CheckOutDate = patch_data.check_out_date
        if patch_data.room_type:
            booking.RoomType = patch_data.room_type
        if patch_data.total_price:
            booking.TotalPrice = patch_data.total_price

        session.commit()

        return {"message": "Booking updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    
@app.get("/hotels")
def get_all_hotel() :
    all_hotel = session.query(Hotel).all()
    return all_hotel


@app.get("/hotels/{hotel_id}")
def get_hotel(hotel_id: int):
    hotel = session.query(Hotel).filter(Hotel.HotelID == hotel_id).first()
    if hotel:
        return HotelResponse(
            hotel_id=hotel.HotelID,
            name=hotel.Name,
            address=hotel.Address,
            phone=hotel.Phone,
            email=hotel.Email,
            rating=hotel.Rating,
            capacity=hotel.Capacity
        )
    else:
        raise HTTPException(status_code=404, detail="Hotel not found")

@app.post("/hotels")
def create_hotel(hotel: HotelRequest):
    new_hotel = Hotel(
        Name=hotel.name,
        Address=hotel.address,
        Phone=hotel.phone,
        Email=hotel.email,
        Rating=hotel.rating,
        Capacity=hotel.capacity
    )
    session.add(new_hotel)
    session.commit()
    session.refresh(new_hotel)
    return HotelResponse(
        hotel_id=new_hotel.HotelID,
        name=new_hotel.Name,
        address=new_hotel.Address,
        phone=new_hotel.Phone,
        email=new_hotel.Email,
        rating=new_hotel.Rating,
        capacity=new_hotel.Capacity
    )
    

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    hotel = session.query(Hotel).filter(Hotel.HotelID == hotel_id).first()
    if hotel:
        session.delete(hotel)
        session.commit()
        return {"message": "Hotel deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Hotel not found")

@app.patch("/hotels/{hotel_id}")
def patch_hotel(hotel_id: int, patch_data: HotelPatchRequest):
    hotel = session.query(Hotel).filter(Hotel.HotelID == hotel_id).first()
    if hotel:
        # Update the hotel with the provided patch data
        if patch_data.name:
            hotel.Name = patch_data.name
        if patch_data.address:
            hotel.Address = patch_data.address
        if patch_data.phone:
            hotel.Phone = patch_data.phone
        if patch_data.email:
            hotel.Email = patch_data.email
        if patch_data.rating:
            hotel.Rating = patch_data.rating
        if patch_data.capacity:
            hotel.Capacity = patch_data.capacity

        session.commit()

        return {"message": "Hotel updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Hotel not found")