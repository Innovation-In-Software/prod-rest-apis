"""
MD291 Lab: Virtual Environments & Data Validation with Pydantic
Starter code.

Look for the six numbered TODOs below and fill in the blank lines.
Each one is small. Tips are right above every TODO to guide you.
When all six are done, run:  python starter.py
"""
import time
from datetime import datetime
from functools import wraps

import pandas as pd  # third-party library: proves the venv is isolated
from pydantic import BaseModel, EmailStr, field_validator, ValidationError


# ---------------------------------------------------------------------------
# PART 3 — Decorator
# ---------------------------------------------------------------------------
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        # TODO 1: print how long the function took.
        # TIP: use an f-string. 'elapsed' (above) holds the seconds.
        #      Example format:  f"done in {elapsed:.3f}s"
        print("")  # <-- put your f-string inside these parentheses

        return result
    return wrapper


# ---------------------------------------------------------------------------
# PART 4 — Pydantic model
# ---------------------------------------------------------------------------
class Employee(BaseModel):
    employee_id: int
    name: str
    email: EmailStr
    age: int
    department: str
    salary: float
    start_date: str

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        # (already written for you) reject blank names
        if not v.strip():
            raise ValueError("name cannot be blank")
        return v

    @field_validator("age")
    @classmethod
    def age_in_range(cls, v: int) -> int:
        # TODO 2: reject ages that are not between 0 and 120.
        # TIP: if the number is out of range, raise ValueError("...").
        #      Fill in the condition after 'if'. Chained compare works:
        #      0 <= v <= 120  is True only when v is in range.
        if not (____):                      # <-- replace ____ with the check
            raise ValueError(f"age {v} is out of range 0-120")
        return v

    @field_validator("salary")
    @classmethod
    def salary_non_negative(cls, v: float) -> float:
        # TODO 3: reject a salary below zero.
        # TIP: compare v to 0. Raise ValueError if it's negative.
        if v < ____:                        # <-- replace ____ with the number
            raise ValueError(f"salary {v} cannot be negative")
        return v

    @field_validator("department")
    @classmethod
    def known_department(cls, v: str) -> str:
        # TODO 5: reject any department not in our list of valid ones.
        # TIP: the 'in' operator checks membership:  v in valid_depts
        #      We want to reject when v is NOT in the list, so use 'not in'.
        valid_depts = ["Engineering", "Marketing", "Sales", "Finance"]
        if v ____ valid_depts:              # <-- replace ____ with:  not in
            raise ValueError(f"unknown department '{v}'")
        return v

    @field_validator("start_date")
    @classmethod
    def valid_iso_date(cls, v: str) -> str:
        # TODO 4: confirm the date looks like YYYY-MM-DD (e.g. 2021-07-01).
        # TIP: datetime.strptime(v, "____") raises ValueError on a bad date.
        #      The format codes are:  %Y = year, %m = month, %d = day.
        #      So the pattern string is  "%Y-%m-%d"  (keep the dashes).
        try:
            datetime.strptime(v, "____")    # <-- replace ____ with the pattern
        except ValueError:
            raise ValueError(f"start_date '{v}' is not YYYY-MM-DD")
        return v


# ---------------------------------------------------------------------------
# PART 5 — Load & validate  (already written for you — just read it)
# ---------------------------------------------------------------------------
@timer
def load_employees(path: str) -> list[Employee]:
    valid: list[Employee] = []
    errors = 0
    df = pd.read_csv(path, dtype=str).fillna("")
    for _, row in df.iterrows():
        try:
            valid.append(Employee(**row.to_dict()))
        except ValidationError as exc:
            errors += 1
            first = exc.errors()[0]
            print(f"  row {row['employee_id']}: {first['msg']}")
    print(f"Valid: {len(valid)}  |  Rejected: {errors}")
    return valid


if __name__ == "__main__":
    employees = load_employees("employees_messy.csv")
    print("\n--- First valid employees ---")
    for e in employees[:5]:
        print(e.name, e.email, e.department)

    # TODO 6: count how many valid employees are in each department.
    # TIP: loop over 'employees'. For each one, add 1 to its department's
    #      count in the dict. dict.get(key, 0) returns 0 if the key isn't
    #      there yet, so this line handles the "first time seen" case too.
    print("\n--- Headcount by department ---")
    counts: dict[str, int] = {}
    for e in employees:
        counts[e.department] = counts.get(e.department, 0) ____ 1   # <-- replace ____ with:  +
    for dept, n in counts.items():
        print(f"{dept}: {n}")