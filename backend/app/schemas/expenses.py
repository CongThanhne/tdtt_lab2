from pydantic import BaseModel

class ExpenseBase(BaseModel):
    name: str
    amount: float
    date: str
    category: str = "Khác"

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: str
    user_id: str
