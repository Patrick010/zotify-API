import time
from collections import deque
from typing import List, Dict, Optional
from zotify_api.schemas.download import DownloadJob, DownloadJobStatus, DownloadQueueStatus

class DownloadsService:
    """
    Manages the download queue and the status of download jobs.
    NOTE: This is a simple in-memory implementation. A persistent queue
    is a required future enhancement.
    """
    def __init__(self):
        self.queue: deque[DownloadJob] = deque()
        self.jobs: Dict[str, DownloadJob] = {}

    def add_downloads_to_queue(self, track_ids: List[str]) -> List[DownloadJob]:
        """Creates new download jobs and adds them to the queue."""
        new_jobs = []
        for track_id in track_ids:
            job = DownloadJob(track_id=track_id)
            self.queue.append(job)
            self.jobs[job.job_id] = job
            new_jobs.append(job)
        return new_jobs

    def get_queue_status(self) -> DownloadQueueStatus:
        """Returns the current status of the download queue."""
        status_counts = {
            DownloadJobStatus.PENDING: 0,
            DownloadJobStatus.IN_PROGRESS: 0,
            DownloadJobStatus.COMPLETED: 0,
            DownloadJobStatus.FAILED: 0,
        }
        for job in self.jobs.values():
            if job.status in status_counts:
                status_counts[job.status] += 1

        return DownloadQueueStatus(
            total_jobs=len(self.jobs),
            pending=status_counts[DownloadJobStatus.PENDING],
            completed=status_counts[DownloadJobStatus.COMPLETED],
            failed=status_counts[DownloadJobStatus.FAILED],
            jobs=list(self.jobs.values())
        )

    def process_download_queue(self, force_fail: bool = False) -> Optional[DownloadJob]:
        """
        Processes one job from the download queue.
        This method is designed to be called manually to simulate a background worker.
        """
        if not self.queue:
            return None

        job = self.queue.popleft()
        job.status = DownloadJobStatus.IN_PROGRESS

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

        return job

    def retry_failed_jobs(self) -> DownloadQueueStatus:
        """Resets the status of all failed jobs to pending and re-queues them."""
        for job in self.jobs.values():
            if job.status == DownloadJobStatus.FAILED:
                job.status = DownloadJobStatus.PENDING
                job.error_message = None
                self.queue.append(job)
        return self.get_queue_status()


# --- FastAPI Dependency ---

# A simple singleton pattern to ensure we use the same service instance
downloads_service_instance = DownloadsService()

def get_downloads_service():
    return downloads_service_instance
