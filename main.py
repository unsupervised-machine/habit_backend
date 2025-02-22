# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import auth, users, payments, habits, completions

app = FastAPI()

# Enable CORS (adjust allow_origins as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the SQLite database
init_db()

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(habits.router, prefix="/habits", tags=["habits"])
app.include_router(completions.router, prefix="/completions", tags=["completions"])


# Dead root endpoint: returns a default message indicating there's no content.
@app.get("/")
def read_root():
    return {"message": "Dead root. No content available here."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
