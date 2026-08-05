from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

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



def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    try:
        logger.info(f"Login attempt: {email}")

        users = db.query(User).all()

        logger.info("Users in database:")
        for u in users:
            logger.info(f"{u.id} | {u.username} | {u.email}")

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if user is None:
            logger.warning(f"Login failed. Email not found: {email}")
            return None

        if not verify_password(password, user.hashed_password):
            logger.warning(f"Incorrect password for {email}")
            return None

        logger.info(f"User authenticated successfully: {email}")
        return user

    except SQLAlchemyError as e:
        logger.exception(f"Database error during login: {e}")
        raise