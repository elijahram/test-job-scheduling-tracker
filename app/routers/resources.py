from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db, require_role
from app.models import Resource, User
from app.schemas import ResourceCreate, ResourceOut

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("/", response_model=list[ResourceOut])
def get_resources(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    resources = db.query(Resource).all()
    return resources


@router.post("/", response_model=ResourceOut, status_code=201)
def create_resource(
    resource: ResourceCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("test_lead", "admin"))],
):
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
