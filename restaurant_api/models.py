from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(String)
    hours_of_operation = Column(String)
    owner_id = Column(Integer)  # Assuming an external User service

    menu_items = relationship("MenuItem", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")

class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    available = Column(Boolean, default=True)

    restaurant = relationship("Restaurant", back_populates="menu_items")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    status = Column(String, default="pending")

    restaurant = relationship("Restaurant", back_populates="orders")
