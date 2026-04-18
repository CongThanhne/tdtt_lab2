from fastapi import APIRouter, Depends
from typing import List
from app.dependencies.auth import get_current_user
from app.schemas.auth import UserSchema
from app.schemas.expenses import ExpenseCreate, Expense
from app.services.firestore_service import FirestoreService

router = APIRouter()

@router.post("/", response_model=Expense)
def create_expense(expense: ExpenseCreate, user: UserSchema = Depends(get_current_user)):
    data = expense.model_dump()
    data["user_id"] = user.uid
    result = FirestoreService.create_expense(data)
    return Expense(**result)

@router.get("/", response_model=List[Expense])
def get_expenses(user: UserSchema = Depends(get_current_user)):
    return FirestoreService.get_expenses_by_user(user.uid)

@router.delete("/{expense_id}")
def delete_expense(expense_id: str, user: UserSchema = Depends(get_current_user)):
    from fastapi import HTTPException
    success = FirestoreService.delete_expense(expense_id, user.uid)
    if not success:
        raise HTTPException(status_code=400, detail="Không tìm thấy khoản chi hoặc không có quyền.")
    return {"message": "Đã xóa khoản chi."}
