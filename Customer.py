from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import create_database, Customer
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
class CustomerPatchRequest(BaseModel):
    name: str = None
    email: str = None
    phone: str = None
    address: str = None     
    

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
