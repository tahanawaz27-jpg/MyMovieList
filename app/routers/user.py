from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.jwt_handler import create_access_token
from app.database import SessionLocal
from app.schemas.user import (
    UserCreate,
    UserResponse,
    Token,
)
from app.services import user_service
from app.utils.logger import logger

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ---------------- REGISTER ---------------- #

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        logger.info(
            f"Registering user: {user.email}"
        )

        result = user_service.create_user(
            db,
            user,
        )

        if result == "email":
            logger.warning(
                f"Registration failed. Email already exists: {user.email}"
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

        if result == "username":
            logger.warning(
                f"Registration failed. Username already exists: {user.username}"
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken.",
            )

        logger.info(
            f"User registered successfully: {user.email}"
        )

        return result

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Registration failed: {e}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to register user.",
        )


# ---------------- LOGIN ---------------- #

@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        logger.info(
            f"Login attempt: {form_data.username}"
        )

        existing_user = user_service.authenticate_user(
            db,
            form_data.username,
            form_data.password,
        )

        if existing_user is None:
            logger.warning(
                f"Failed login attempt: {form_data.username}"
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        access_token = create_access_token(
            {
                "user_id": existing_user.id,
                "email": existing_user.email,
            }
        )

        logger.info(
            f"User logged in successfully: {existing_user.email}"
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Login failed: {e}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to login.",
        )