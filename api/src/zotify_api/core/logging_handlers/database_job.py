from typing import Dict, Any
from ..log_service import BaseLogHandler
from ...database.session import get_session
from ...database.models import JobLog


class DatabaseJobHandler(BaseLogHandler):
    """A log handler that writes job status updates to the database."""

    def can_handle(self, level: str) -> bool:
        return level.upper() == "JOB_STATUS"

    def handle(self, level: str, message: str, extra: Dict[str, Any] = None):
        extra = extra or {}
        job_id = extra.get("job_id")
        if not job_id:
            return

        with get_session() as session:
            job_log = session.query(JobLog).filter(JobLog.job_id == job_id).first()
            if not job_log:
                job_log = JobLog(
                    job_id=job_id,
                    job_type=extra.get("job_type"),
                    status=message,
                    progress=extra.get("progress", 0),
                    details=extra.get("details", {}),
                )
                session.add(job_log)
            else:
                job_log.status = message
                if "progress" in extra:
                    job_log.progress = extra["progress"]
                if "details" in extra:
                    job_log.details = extra["details"]

            session.commit()
