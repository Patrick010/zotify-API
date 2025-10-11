# ID: API-092
import time
from typing import List, cast

from sqlalchemy.orm import Session

from zotify_api.database import crud, models
from zotify_api.schemas import download as schemas


def add_downloads_to_queue(
    db: Session, track_ids: List[str]
) -> List[models.DownloadJob]:
    """Creates new download jobs and adds them to the database queue."""
    new_jobs = []
    for track_id in track_ids:
        job_create = schemas.DownloadJobCreate(track_id=track_id)
        job = crud.create_download_job(db=db, job=job_create)
        new_jobs.append(job)
    return new_jobs


def get_queue_status(db: Session) -> schemas.DownloadQueueStatus:
    """Returns the current status of the download queue from the database."""
    all_jobs = crud.get_all_download_jobs(db=db)

    status_counts = {
        schemas.DownloadJobStatus.PENDING: 0,
        schemas.DownloadJobStatus.IN_PROGRESS: 0,
        schemas.DownloadJobStatus.COMPLETED: 0,
        schemas.DownloadJobStatus.FAILED: 0,
    }
    for job in all_jobs:
        # The status in the DB is a string, so we need to convert it back to the Enum
        status_enum = schemas.DownloadJobStatus(job.status)
        if status_enum in status_counts:
            status_counts[status_enum] += 1

    return schemas.DownloadQueueStatus(
        total_jobs=len(all_jobs),
        pending=status_counts[schemas.DownloadJobStatus.PENDING],
        completed=status_counts[schemas.DownloadJobStatus.COMPLETED],
        failed=status_counts[schemas.DownloadJobStatus.FAILED],
        jobs=all_jobs,
    )


def process_download_queue(
    db: Session, force_fail: bool = False
) -> models.DownloadJob | None:
    """
    Processes one job from the download queue.
    This method is designed to be called manually to simulate a background worker.
    """
    job = crud.get_next_pending_download_job(db=db)
    if not job:
        return None

    crud.update_download_job_status(
        db=db, job=job, status=schemas.DownloadJobStatus.IN_PROGRESS
    )

    try:
        # Simulate the download process
        time.sleep(0.1)  # Simulate I/O
        if force_fail:
            raise ValueError("Forced failure for testing.")

        # Simulate a successful download
        job = crud.update_download_job_status(
            db=db, job=job, status=schemas.DownloadJobStatus.COMPLETED, progress=1.0
        )
    except Exception as e:
        job = crud.update_download_job_status(
            db=db, job=job, status=schemas.DownloadJobStatus.FAILED, error=str(e)
        )

    return job


def retry_failed_jobs(db: Session) -> int:
    """Resets the status of all failed jobs to pending in the database."""
    return cast(int, crud.retry_failed_download_jobs(db=db))
