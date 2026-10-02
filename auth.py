from jose import jwt
from datetime import datetime
from datetime import timedelta

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=5)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


