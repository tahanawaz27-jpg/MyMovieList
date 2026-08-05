from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.jwt_handler import verify_token
from app.database import SessionLocal
from app.models.user import User
from app.utils.logger import logger

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = verify_token(token)

        if payload is None:
            logger.warning("Invalid JWT token.")

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token.",
            )

        user = (
            db.query(User)
            .filter(
                User.id == payload["user_id"]
            )
            .first()
        )

        if user is None:
            logger.warning(
                f"User {payload['user_id']} not found."
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found.",
            )

        logger.info(
            f"Authenticated user {user.email}"
        )

        return user

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Authentication failed: {e}"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed.",
        )