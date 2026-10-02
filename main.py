from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from database import Base

import models

from routes.auth_routes import router as auth_router
from routes.complaint_routes import router as complaint_router


app = FastAPI()

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth_router)
app.include_router(complaint_router)


@app.get("/")
def home():
    return {
        "message": "CampusCare Backend Running"
    }