import datetime
import uuid
from typing import List

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    Column,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# --- Association Table for Playlists and Tracks (Many-to-Many) ---

playlist_track_association = Table(
    "playlist_track_association",
    Base.metadata,
    Column("playlist_id", String, ForeignKey("playlists.id"), primary_key=True),
    Column("track_id", String, ForeignKey("tracks.id"), primary_key=True),
)

# --- ORM Models ---


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    # A simple role system for future use
    role: Mapped[str] = mapped_column(String, default="user", nullable=False)


class SpotifyToken(Base):
    __tablename__ = "spotify_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Simple auto-incrementing ID
    # For multi-user support
    user_id: Mapped[str | None] = mapped_column(String, ForeignKey("users.id"), nullable=True)
    access_token: Mapped[str] = mapped_column(String, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Track(Base):
    __tablename__ = "tracks"
    id: Mapped[str] = mapped_column(String, primary_key=True)  # Spotify track ID
    name: Mapped[str | None] = mapped_column(
        String, nullable=True
    )  # Optional: store track name for convenience
    playlists: Mapped[List["Playlist"]] = relationship(
        "Playlist", secondary=playlist_track_association, back_populates="tracks"
    )


class Playlist(Base):
    __tablename__ = "playlists"
    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    tracks: Mapped[List["Track"]] = relationship(
        "Track", secondary=playlist_track_association, back_populates="playlists"
    )


class DownloadJob(Base):
    __tablename__ = "download_jobs"
    job_id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    track_id: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)


class JobLog(Base):
    __tablename__ = "job_logs"
    job_id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    job_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
