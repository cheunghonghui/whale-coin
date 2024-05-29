from sqlalchemy import Column, Integer, Float, VARCHAR, DateTime
from app.database import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(200), nullable=False)
    email = Column(VARCHAR(200), nullable=False)
    password = Column(VARCHAR(500), nullable=True)
    phone = Column(VARCHAR(80))
    gender = Column(VARCHAR(32))
    location = Column(VARCHAR(32))
    role = Column(VARCHAR(32))
    value = Column(Float, default=0.0)
    avantar = Column(VARCHAR(256))
    desc = Column(VARCHAR(1000))
    register_time = Column(DateTime)
    last_login_time = Column(DateTime)

class Register(Base):
    __tablename__ = 'register'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(200), nullable=False)
    email = Column(VARCHAR(200), nullable=False)
    password = Column(VARCHAR(500), nullable=True)
    phone = Column(VARCHAR(80))
    notes = Column(VARCHAR(500))
    register_time = Column(DateTime)
