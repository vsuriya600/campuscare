from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)

    institutional_id = Column(
        String(50),
        unique=True,
        nullable=False
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        Enum(
            "student",
            "staff",
            "warden",
            "admin"
        ),
        nullable=False
    )


class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )

    title = Column(
        String(150),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    status = Column(
        Enum(
            "pending",
            "assigned",
            "resolved"
        ),
        default="pending"
    )

    is_spam = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )


class Location(Base):
    __tablename__ = "locations"

    location_id = Column(
        Integer,
        primary_key=True
    )

    complaint_id = Column(
        Integer,
        ForeignKey("complaints.complaint_id")
    )

    zone = Column(
        Enum(
            "hostel",
            "mess_canteen",
            "admin",
            "campus"
        ),
        nullable=False
    )

    building_name = Column(
        String(100),
        nullable=False
    )

    room_or_area = Column(
        String(100),
        nullable=False
    )