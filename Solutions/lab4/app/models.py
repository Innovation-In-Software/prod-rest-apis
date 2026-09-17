"""Data models for the Loans API.

This mirrors the models.py that `fastapi-codegen` generates from the finished
sample.yaml (slide 9). Field names, types, and the status enum all come straight
from the spec's LoanApplication schema.
"""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Status(str, Enum):
    """Allowed values for a loan's status (from the spec's enum)."""
    pending = "pending"
    approved = "approved"
    denied = "denied"


class LoanApplication(BaseModel):
    """One loan application, exactly as described in the spec.

    Required: applicant_name, amount, term_months.
    status defaults to 'pending' so new applications start pending automatically.
    """
    applicant_name: str
    amount: float
    term_months: int
    status: Optional[Status] = Status.pending
