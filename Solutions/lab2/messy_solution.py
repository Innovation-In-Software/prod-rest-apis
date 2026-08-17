"""
MD291 Lab 2 (labs\lab2): Virtual Environments & Data Validation with Pydantic
SOLUTION — all six TODOs completed.
Run:  python messy_solution.py
"""
import time
from datetime import datetime
from functools import wraps

import pandas as pd
from pydantic import BaseModel, EmailStr, field_validator, ValidationError


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__}: {elapsed:.3f}s")          # TODO 1
        return result
    return wrapper


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
        if not v.strip():
            raise ValueError("name cannot be blank")
        return v

    @field_validator("age")
    @classmethod
    def age_in_range(cls, v: int) -> int:
        if not (0 <= v <= 120):                            # TODO 2
            raise ValueError(f"age {v} is out of range 0-120")
        return v

    @field_validator("salary")
    @classmethod
    def salary_non_negative(cls, v: float) -> float:
        if v < 0:                                          # TODO 3
            raise ValueError(f"salary {v} cannot be negative")
        return v

    @field_validator("department")
    @classmethod
    def known_department(cls, v: str) -> str:
        valid_depts = ["Engineering", "Marketing", "Sales", "Finance"]
        if v not in valid_depts:                           # TODO 5
            raise ValueError(f"unknown department '{v}'")
        return v

    @field_validator("start_date")
    @classmethod
    def valid_iso_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")               # TODO 4
        except ValueError:
            raise ValueError(f"start_date '{v}' is not YYYY-MM-DD")
        return v


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

    print("\n--- Headcount by department ---")
    counts: dict[str, int] = {}
    for e in employees:
        counts[e.department] = counts.get(e.department, 0) + 1   # TODO 6
    for dept, n in counts.items():
        print(f"{dept}: {n}")
