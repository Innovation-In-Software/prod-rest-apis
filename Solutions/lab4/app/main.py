from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Status(str, Enum):
    pending = "pending"
    approved = "approved"
    denied = "denied"


class LoanApplication(BaseModel):
    applicant_name: str
    amount: float
    term_months: int
    status: Status = Status.pending


app = FastAPI()
loans: list = []


@app.post("/loans", status_code=201)
def create_loan(application: LoanApplication):
    loans.append(application)
    return application


@app.get("/loans")
def list_loans(status: Status | None = None):
    if status:
        return [l for l in loans if l.status == status]
    return loans


@app.get("/loans/{loan_id}")
def get_loan(loan_id: int):
    for l in loans:
        if l.loan_id == loan_id:
            return l
    raise HTTPException(status_code=404, detail="Loan not found")
