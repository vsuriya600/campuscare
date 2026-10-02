from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import get_db
from models import User

from utils.security import hash_password
from utils.security import verify_password

from auth import create_token

router = APIRouter()


@router.post("/register")
def register(data: dict, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.institutional_id == data["institutional_id"]
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = User(
        institutional_id=data["institutional_id"],
        full_name=data["full_name"],
        password_hash=hash_password(data["password"]),
        role=data["role"]
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.institutional_id == data["institutional_id"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        data["password"],
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_token({
        "user_id": user.user_id,
        "role": user.role
    })

    return {

    "access_token":  token,

    "role": user.role,

    "user_id": user.user_id,

    "full_name": user.full_name
}