
# create_tables.py

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    Enum,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    func
)
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv
import os

# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Example:
# DATABASE_URL=mysql+pymysql://username:password@host:3306/database_name

# =========================================================
# DATABASE ENGINE
# =========================================================

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Base = declarative_base()

# =========================================================
# USERS TABLE
# =========================================================

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)

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
            "admin",
            name="user_roles"
        ),
        nullable=False
    )

    complaints = relationship(
        "Complaint",
        back_populates="user",
        cascade="all, delete"
    )

# =========================================================
# COMPLAINTS TABLE
# =========================================================

class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
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
            "resolved",
            name="complaint_status"
        ),
        default="pending",
        nullable=False
    )

    is_spam = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )

    user = relationship(
        "User",
        back_populates="complaints"
    )

    location = relationship(
        "Location",
        back_populates="complaint",
        uselist=False,
        cascade="all, delete"
    )

# =========================================================
# LOCATIONS TABLE
# =========================================================

class Location(Base):
    __tablename__ = "locations"

    location_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    complaint_id = Column(
        Integer,
        ForeignKey("complaints.complaint_id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    zone = Column(
        Enum(
            "hostel",
            "mess_canteen",
            "admin",
            "campus",
            name="zone_types"
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

    complaint = relationship(
        "Complaint",
        back_populates="location"
    )

# =========================================================
# CREATE TABLES
# =========================================================

if __name__ == "__main__":
    print("\nCreating tables...\n")

    Base.metadata.create_all(engine)

    print("\nAll tables created successfully!")