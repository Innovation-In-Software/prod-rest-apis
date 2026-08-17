from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Pydantic model — defines the shape of a transaction amount
class Transaction(BaseModel):
    amount: float

# Global balance variable
balance: float = 100.0

# GET — return the current balance
@app.get("/balance")
def get_balance():
    return balance

# POST — withdraw an amount from the balance
@app.post("/withdrawal")
def withdrawal(transaction: Transaction):
    global balance
    if balance - transaction.amount < 0:
        return "withdrawal would overdraw account"
    balance -= transaction.amount
    return balance

# POST — deposit an amount into the balance
@app.post("/deposit")
def deposit(transaction: Transaction):
    global balance
    balance += transaction.amount
    return balance