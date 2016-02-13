import datetime
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import String, Date, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import backref

Base = declarative_base()


class User(Base):
    __tablename__ = 'cataloguser'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    accounttype = Column(String(50), nullable=False)
    isActive = Column(Boolean, nullable=False, default=True)
    lastlogin = Column(Date)
    pictureurl = Column(String(250))
    password = Column(String(10))
    created = Column(DateTime, default=datetime.datetime.now)
    lastupdated = Column(DateTime, onupdate=datetime.datetime.now)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'email': self.email,
            'accounttype': self.accounttype,
            'isActive': self.isActive,
            'lastlogin': self.lastlogin,
            'pictureurl': self.pictureurl,
            'lastupdated': self.lastupdated,
            'created': self.created
        }


class Categories(Base):
    __tablename__ = 'categories'

    name = Column(String(255), nullable=False)
    parent = Column(Integer)
    isActive = Column(Boolean, nullable=False, default=True)
    # adding a column for easy display
    # This can also be handled by a query at run time
    hasChildren = Column(Boolean, nullable=False, default=False)
    created = Column(DateTime, default=datetime.datetime.now)
    lastupdated = Column(DateTime, onupdate=datetime.datetime.now)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'parent': self.parent,
            'isActive': self.isActive,
            'hasChildren': self.hasChildren,
            'created': self.created,
            'lastupdated': self.lastupdated,
            'id': self.id
        }


class Items(Base):
    __tablename__ = 'items'

    name = Column(String(255), nullable=False)
    description = Column(String(2500), nullable=False)
    pricerange = Column(String(255), nullable=False)
    pictureurl = Column(String(1000), nullable=False)
    isActive = Column(Boolean, nullable=False, default=True)
    created = Column(DateTime, default=datetime.datetime.now)
    lastupdated = Column(DateTime, onupdate=datetime.datetime.now)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    category = relationship(Categories,
                            backref=backref("items", cascade="all,delete"))
    user = relationship(User,
                        backref=backref("items", cascade="all,delete"))
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'pricerange': self.pricerange,
            'isActive': self.isActive,
            'pictureurl': self.pictureurl,
            'created': self.created,
            'lastupdated': self.lastupdated,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'id': self.id
        }


# These line should be at the end of the file.
engine = create_engine('postgresql://catalogadmin:catalogadmin@localhost/catalogdb')
Base.metadata.create_all(engine)
