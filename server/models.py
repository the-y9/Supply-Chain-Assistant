from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# DB Setup
DATABASE_URL = "sqlite:///./app.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    active = Column(Boolean, default=True)


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    category = Column(String(10))
    name = Column(String(80), unique=True)
    description = Column(String(255))


class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    region_id = Column(Integer, ForeignKey("regions.id"))

    user = relationship("User")
    role = relationship("Role")
    region = relationship("Region")


class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String)

    user = relationship("User")

