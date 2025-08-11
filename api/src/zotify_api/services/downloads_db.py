import sqlite3
import os
from typing import List, Optional, Tuple
from contextlib import contextmanager
from zotify_api.schemas.download import DownloadJob, DownloadJobStatus

# --- Constants ---
STORAGE_DIR = "api/storage"
DB_FILE = os.path.join(STORAGE_DIR, "downloads.db")

# --- Database Initialization ---

def init_db():
    """Initializes the database and creates the 'jobs' table if it doesn't exist."""
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                track_id TEXT NOT NULL,
                status TEXT NOT NULL,
                progress REAL,
                created_at TIMESTAMP NOT NULL,
                error_message TEXT
            )
        """)
        conn.commit()

# --- Database Connection Context Manager ---

@contextmanager
def get_db_connection():
    """Provides a database connection."""
    conn = sqlite3.connect(DB_FILE)
    try:
        yield conn
    finally:
        conn.close()

# --- CRUD Operations ---

def add_job_to_db(job: DownloadJob):
    """Adds a new download job to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO jobs (job_id, track_id, status, progress, created_at, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                job.job_id,
                job.track_id,
                job.status.value,
                job.progress,
                job.created_at,
                job.error_message,
            ),
        )
        conn.commit()

def get_job_from_db(job_id: str) -> Optional[DownloadJob]:
    """Retrieves a single download job from the database by its ID."""
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
        row = cursor.fetchone()
        if row:
            return DownloadJob(**row)
    return None

def get_all_jobs_from_db() -> List[DownloadJob]:
    """Retrieves all download jobs from the database."""
    jobs = []
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs ORDER BY created_at DESC")
        rows = cursor.fetchall()
        for row in rows:
            jobs.append(DownloadJob(**row))
    return jobs

def update_job_in_db(job: DownloadJob):
    """Updates an existing job in the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE jobs
            SET status = ?, progress = ?, error_message = ?
            WHERE job_id = ?
            """,
            (job.status.value, job.progress, job.error_message, job.job_id),
        )
        conn.commit()

def get_next_pending_job_from_db() -> Optional[DownloadJob]:
    """Retrieates the oldest pending job from the database."""
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM jobs WHERE status = ? ORDER BY created_at ASC LIMIT 1",
            (DownloadJobStatus.PENDING.value,),
        )
        row = cursor.fetchone()
        if row:
            return DownloadJob(**row)
    return None

def update_failed_jobs_to_pending_in_db() -> int:
    """Resets the status of all failed jobs to 'pending' and returns the count."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE jobs SET status = ?, error_message = NULL WHERE status = ?",
            (DownloadJobStatus.PENDING.value, DownloadJobStatus.FAILED.value),
        )
        conn.commit()
        return cursor.rowcount
