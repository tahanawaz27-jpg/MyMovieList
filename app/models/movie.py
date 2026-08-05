

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    director = Column(
        String,
        nullable=False,
    )

    genre = Column(
        String,
        nullable=False,
    )

    release_year = Column(Integer)

    rating = Column(Float)

    watched = Column(
        Boolean,
        default=False,
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="movies",
    )