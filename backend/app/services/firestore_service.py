import uuid
from app.core.firebase_config import get_db

class FirestoreService:
    @staticmethod
    def create_expense(expense_data: dict) -> dict:
        db = get_db()
        if db:
            doc_ref = db.collection("expenses").document()
            doc_ref.set(expense_data)
            expense_data["id"] = doc_ref.id
        else:
            expense_data["id"] = str(uuid.uuid4())
        return expense_data

    @staticmethod
    def get_expenses_by_user(user_id: str) -> list:
        db = get_db()
        expenses = []
        if db:
            docs = db.collection("expenses").where("user_id", "==", user_id).stream()
            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                expenses.append(data)
        return expenses

    @staticmethod
    def delete_expense(expense_id: str, user_id: str) -> bool:
        db = get_db()
        if db:
            doc_ref = db.collection("expenses").document(expense_id)
            doc = doc_ref.get()
            # Kiem tra dung giao dich cua user moi xoa
            if doc.exists and doc.to_dict().get("user_id") == user_id:
                doc_ref.delete()
                return True
        return False
