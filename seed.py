import random
from faker import Faker
from models import Customer, session

if __name__ == '__main__':

    fake = Faker()
    
    customers = []
    for i in range(10):
        customer = Customer(
            Name = fake.unique.name(),
            Email = fake.unique.email(),
            Phone = random.randint(2547124532,2547980123),
            Address = fake.unique.address()
        )
        
        session.add(customer)
        session.commit()
        customers.append(customer)

