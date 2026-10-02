from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import get_db

from models import Complaint
from models import Location

router = APIRouter()


# ==========================================
# CREATE COMPLAINT
# ==========================================

@router.post("/complaints")
def create_complaint(
    data: dict,
    db: Session = Depends(get_db)
):

    # Create complaint
    new_complaint = Complaint(
        user_id=data["user_id"],
        title=data["title"],
        description=data["description"]
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    # Create location
    new_location = Location(
        complaint_id=new_complaint.complaint_id,
        zone=data["zone"],
        building_name=data["building_name"],
        room_or_area=data["room_or_area"]
    )

    db.add(new_location)
    db.commit()

    return {
        "message": "Complaint submitted successfully"
    }


# ==========================================
# GET USER COMPLAINTS
# ==========================================

@router.get("/complaints/user/{user_id}")
def get_user_complaints(
    user_id: int,
    db: Session = Depends(get_db)
):

    complaints = db.query(Complaint).filter(
        Complaint.user_id == user_id
    ).all()

    result = []

    for complaint in complaints:

        location = db.query(Location).filter(
            Location.complaint_id == complaint.complaint_id
        ).first()

        result.append({
            "complaint_id": complaint.complaint_id,
            "title": complaint.title,
            "description": complaint.description,
            "status": complaint.status,
            "zone": location.zone if location else None,
            "building_name": location.building_name if location else None,
            "room_or_area": location.room_or_area if location else None,
            "created_at": complaint.created_at
        })

    return result


# ==========================================
# GET COMPLAINTS BY ZONE
# ==========================================

@router.get("/complaints/zone/{zone}")
def get_zone_complaints(
    zone: str,
    db: Session = Depends(get_db)
):

    locations = db.query(Location).filter(
        Location.zone == zone
    ).all()

    result = []

    for location in locations:

        complaint = db.query(Complaint).filter(
            Complaint.complaint_id == location.complaint_id
        ).first()

        if complaint:

            result.append({
                "complaint_id": complaint.complaint_id,
                "title": complaint.title,
                "description": complaint.description,
                "status": complaint.status,
                "building_name": location.building_name,
                "room_or_area": location.room_or_area,
                "created_at": complaint.created_at
            })

    return result


# ==========================================
# UPDATE COMPLAINT STATUS
# ==========================================

@router.patch("/complaints/{complaint_id}")
def update_status(
    complaint_id: int,
    data: dict,
    db: Session = Depends(get_db)
):

    complaint = db.query(Complaint).filter(
        Complaint.complaint_id == complaint_id
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    complaint.status = data["status"]

    db.commit()

    return {
        "message": "Complaint status updated"
    }

# ==========================================
# DASHBOARD STATS
# ==========================================

@router.get("/dashboard/stats")
def dashboard_stats(
    db: Session = Depends(get_db)
):

    total = db.query(Complaint).count()

    pending = db.query(Complaint).filter(
        Complaint.status == "pending"
    ).count()

    resolved = db.query(Complaint).filter(
        Complaint.status == "resolved"
    ).count()

    assigned = db.query(Complaint).filter(
        Complaint.status == "assigned"
    ).count()

    return {

        "total": total,

        "pending": pending,

        "resolved": resolved,

        "assigned": assigned
    }



# ==========================================
# GET ALL COMPLAINTS
# ==========================================

@router.get("/complaints")
def get_all_complaints(
    db: Session = Depends(get_db)
):

    complaints = db.query(Complaint).all()

    result = []

    for complaint in complaints:

        location = db.query(Location).filter(
            Location.complaint_id ==
            complaint.complaint_id
        ).first()

        result.append({

            "complaint_id":
            complaint.complaint_id,

            "title":
            complaint.title,

            "description":
            complaint.description,

            "status":
            complaint.status,

            "building_name":
            location.building_name if location else "",

            "room_or_area":
            location.room_or_area if location else ""
        })

    return result