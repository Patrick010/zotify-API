import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .session import Base

# --- Association Table for Playlists and Tracks (Many-to-Many) ---

playlist_track_association = Table(
    "playlist_track_association",
    Base.metadata,
    Column("playlist_id", String, ForeignKey("playlists.id")),
    Column("track_id", String, ForeignKey("tracks.id")),
)

# --- ORM Models ---


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # A simple role system for future use
    role = Column(String, default="user", nullable=False)


class SpotifyToken(Base):
    __tablename__ = "spotify_tokens"
    id = Column(Integer, primary_key=True)  # Simple auto-incrementing ID
    # For multi-user support
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)


class Track(Base):
    __tablename__ = "tracks"
    id = Column(String, primary_key=True)  # Spotify track ID
    name = Column(String, nullable=True)  # Optional: store track name for convenience
    playlists = relationship(
        "Playlist", secondary=playlist_track_association, back_populates="tracks"
    )


class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    tracks = relationship(
        "Track", secondary=playlist_track_association, back_populates="playlists"
    )


class DownloadJob(Base):
    __tablename__ = "download_jobs"
    job_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    track_id = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    progress = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    error_message = Column(String, nullable=True)


class JobLog(Base):
    __tablename__ = "job_logs"
    job_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    progress = Column(Integer, default=0)
    details = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
