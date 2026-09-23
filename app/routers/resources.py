from app.models import Resource
from app.schemas import ResourceCreate, ResourceOut
from app.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("/", response_model=list[ResourceOut])
def get_resources(db: Session = Depends(get_db)):
    resources = db.query(Resource).all()
    return resources


@router.post("/", response_model=ResourceOut)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    db_resource = Resource(**resource.model_dump())

    try:
        db.add(db_resource)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"A resource named '{resource.name}' already exists.",
        )

    db.refresh(db_resource)
    return db_resource
