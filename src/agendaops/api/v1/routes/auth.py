from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from agendaops.core.security import create_access_token, hash_password, verify_password
from agendaops.db.session import get_db
from agendaops.models.user import User
from agendaops.schemas.user import TokenResponse, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    existing = db.scalars(select(User).where(User.username == payload.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=payload.username,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    user = db.scalars(select(User).where(User.username == form.username)).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}