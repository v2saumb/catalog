
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelters'

    name = Column(String(80), nullable=False)
    address = Column(String(250), nullable=False)
    city = Column(String(250))
    state = Column(String(250))
    email = Column(String(200))
    zipCode = Column(String(10))
    website = Column(String(200))
    current_occupancy = Column(Integer, default=0)
    maximum_capacity = Column(Integer, default=5)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'email': self.email,
            'zipCode': self.zipCode,
            'website': self.website,
            'current_occupancy': self.current_occupancy,
            'maximum_capacity': self.maximum_capacity,
            'id': self.id
        }


class Puppy(Base):
    __tablename__ = 'puppies'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    dateOfBirth = Column(Date, nullable=False)
    breed = Column(String(250))
    gender = Column(String(250))
    picture = Column(String)
    weight = Column(Integer)
    shelter_id = Column(Integer, ForeignKey('shelters.id'))
    shelter = relationship(Shelter)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'dateOfBirth': self.dateOfBirth,
            'breed': self.breed,
            'gender': self.gender,
            'picture': self.picture,
            'weight': self.weight,
            'shelter_id': self.shelter_id
        }


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    accounttype = Column(String(50), nullable=False)
    isActive = Column(Boolean, nullable=False, default=True)
    lastlogin = Column(Date)
    pictureurl = Column(String(250))
    password = Column(String(10))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'email': self.email,
            'accounttype': self.accounttype,
            'isActive': self.isActive,
            'lastlogin': self.lastlogin,
            'pictureurl': self.pictureurl
        }

# These line should be at the end of the file.
engine = create_engine('sqlite:///src/catalogdb/animalshelter.db')
Base.metadata.create_all(engine)
