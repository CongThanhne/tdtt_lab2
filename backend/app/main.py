from fastapi import FastAPI
from app.routers import auth, expenses

app = FastAPI(title="Expense Manager API")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])

@app.get("/")
def read_root():
    return {"message": "Expense API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
