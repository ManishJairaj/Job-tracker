from enum import Enum


class JobStatus(str, Enum):
    APPLIED = "Applied"
    INTERVIEW = "Interview"
    OFFERED = "Offered"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"
