import logging
from typing import Any, Dict, List

from zotify_api.database.models import JobLog
from zotify_api.database.session import get_db

from .base import BaseLogHandler

log = logging.getLogger(__name__)

class DatabaseJobHandler(BaseLogHandler):
    """
    A log handler that writes job status updates to the database.
    """

    def __init__(self, levels: List[str]):
        self.levels = [level.upper() for level in levels]
        log.debug(f"DatabaseJobHandler initialized for levels: {self.levels}")

    def can_handle(self, level: str) -> bool:
        return level.upper() in self.levels

    def emit(self, log_record: Dict[str, Any]):
        """
        Creates or updates a job log entry in the database.
        """
        job_id = log_record.get("job_id")
        if not job_id:
            log.error("DatabaseJobHandler requires a 'job_id' in the log record.")
            return

        with get_db() as session:
            try:
                job_log = session.query(JobLog).filter(JobLog.job_id == job_id).first()

                if job_log:
                    # Update existing job
                    job_log.status = log_record.get("status", job_log.status)
                    job_log.progress = log_record.get("progress", job_log.progress)
                    if "details" in log_record:
                        job_log.set_details(log_record["details"])
                else:
                    # Create new job
                    job_log = JobLog(
                        job_id=job_id,
                        job_type=log_record.get("job_type", "UNKNOWN"),
                        status=log_record.get("status", "QUEUED"),
                        progress=log_record.get("progress", 0),
                    )
                    if "details" in log_record:
                        job_log.set_details(log_record["details"])
                    session.add(job_log)

                session.commit()
            except Exception:
                log.exception(
                    "Failed to write to job log in database for job_id: %s", job_id
                )
                session.rollback()
