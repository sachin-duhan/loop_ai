from enum import Enum


class JobStatus(Enum):
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
