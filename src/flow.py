# src/flow.py
from .annotations import query, depends_on, weight

@query("auth_voter")
@weight(1)
def auth_voter(): pass

@query("eligibility_check")
@depends_on("auth_voter")
@weight(1)
def eligibility_check(): pass

@query("submit_vote")
@depends_on("eligibility_check")
@weight(1)
def submit_vote(): pass

@query("audit_review")
@depends_on("submit_vote")
@weight(1)
def audit_review(): pass

@query("finalize_count")
@depends_on("submit_vote")
@depends_on("audit_review")
@weight(1)
def finalize_count(): pass

@depends_on("auth_voter")
@weight(3)
def retry_policy(): pass
