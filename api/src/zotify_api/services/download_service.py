import time
from typing import List, Optional
from zotify_api.schemas.download import DownloadJob, DownloadJobStatus, DownloadQueueStatus
import zotify_api.services.downloads_db as downloads_db

class DownloadsService:
    """
    Manages the download queue and the status of download jobs using a persistent
    SQLite database.
    """

    def add_downloads_to_queue(self, track_ids: List[str]) -> List[DownloadJob]:
        """Creates new download jobs and adds them to the database queue."""
        new_jobs = []
        for track_id in track_ids:
            job = DownloadJob(track_id=track_id)
            downloads_db.add_job_to_db(job)
            new_jobs.append(job)
        return new_jobs

    def get_queue_status(self) -> DownloadQueueStatus:
        """Returns the current status of the download queue from the database."""
        all_jobs = downloads_db.get_all_jobs_from_db()

        status_counts = {
            DownloadJobStatus.PENDING: 0,
            DownloadJobStatus.IN_PROGRESS: 0,
            DownloadJobStatus.COMPLETED: 0,
            DownloadJobStatus.FAILED: 0,
        }
        for job in all_jobs:
            if job.status in status_counts:
                status_counts[job.status] += 1

        return DownloadQueueStatus(
            total_jobs=len(all_jobs),
            pending=status_counts[DownloadJobStatus.PENDING],
            completed=status_counts[DownloadJobStatus.COMPLETED],
            failed=status_counts[DownloadJobStatus.FAILED],
            jobs=all_jobs,
        )

    def process_download_queue(self, force_fail: bool = False) -> Optional[DownloadJob]:
        """
        Processes one job from the download queue.
        This method is designed to be called manually to simulate a background worker.
        """
        job = downloads_db.get_next_pending_job_from_db()
        if not job:
            return None

        job.status = DownloadJobStatus.IN_PROGRESS
        downloads_db.update_job_in_db(job)

        try:
            # Simulate the download process
            time.sleep(0.1)  # Simulate I/O
            if force_fail:
                raise ValueError("Forced failure for testing.")

            # Simulate a successful download
            job.progress = 1.0
            job.status = DownloadJobStatus.COMPLETED
        except Exception as e:
            job.status = DownloadJobStatus.FAILED
            job.error_message = str(e)

        downloads_db.update_job_in_db(job)
        return job

    def retry_failed_jobs(self) -> DownloadQueueStatus:
        """Resets the status of all failed jobs to pending in the database."""
        downloads_db.update_failed_jobs_to_pending_in_db()
        return self.get_queue_status()


# --- FastAPI Dependency ---

# Initialize the database when the application starts
downloads_db.init_db()

# A simple singleton pattern to ensure we use the same service instance
downloads_service_instance = DownloadsService()

def get_downloads_service():
    return downloads_service_instance
