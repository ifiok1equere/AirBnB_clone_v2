#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    # Defining a 1-many relationship with City for DB storage
    cities = relationship(
            "City", back_populates='state',
            cascade='all, delete-orphan'
            )

    @property
    def cities(self):
        """returns the list of City instances"""
        cities = []
        for city in storage.all(City).values():
            if city.state_id == self.id:
                cities.append(city)
        return cities
