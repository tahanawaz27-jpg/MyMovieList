from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from app.models.user import User
from app.schemas.user import (
    UserCreate,
)
from app.auth.hashing import (
    hash_password,
)
from app.utils.logger import logger
from app.auth.hashing import verify_password
def create_user(
    db: Session,
    user: UserCreate,
):
    try:
        # Check if email already exists
        existing_email = (
            db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_email:
            logger.warning(
                f"Registration failed. Email already exists: {user.email}"
            )
            return "email"

        # Check if username already exists
        existing_username = (
            db.query(User)
            .filter(User.username == user.username)
            .first()
        )

        if existing_username:
            logger.warning(
                f"Registration failed. Username already exists: {user.username}"
            )
            return "username"

        # Create new user
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(
                user.password
            ),
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(
            f"User registered successfully: {new_user.email}"
        )

        return new_user

    except SQLAlchemyError as e:
        db.rollback()

        logger.exception(
            f"Database error while creating user: {e}"
        )

        raise

from sqlalchemy import or_


def authenticate_user(
    db: Session,
    username_or_email: str,
    password: str,
):
    try:
        logger.info(
            f"Login attempt: {username_or_email}"
        )

        user = (
            db.query(User)
            .filter(
                or_(
                    User.email == username_or_email,
                    User.username == username_or_email,
                )
            )
            .first()
        )

        if user is None:
            logger.warning(
                f"Login failed. User not found: {username_or_email}"
            )
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            logger.warning(
                f"Incorrect password for {username_or_email}"
            )
            return None

        logger.info(
            f"User authenticated successfully: {user.email}"
        )

        return user

    except SQLAlchemyError as e:
        logger.exception(
            f"Database error during login: {e}"
        )
        raise