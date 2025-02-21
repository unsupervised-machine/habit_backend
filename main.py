# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import auth, reminders, big_tasks, sub_tasks, daily_big_task_status, daily_sub_task_status, big_task_attributes, sub_task_attributes

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
app.include_router(big_tasks.router, prefix="/api")
app.include_router(sub_tasks.router, prefix="/api")
app.include_router(daily_big_task_status.router, prefix="/api")
app.include_router(daily_sub_task_status.router, prefix="/api")
app.include_router(big_task_attributes.router, prefix="/api")
app.include_router(sub_task_attributes.router, prefix="/api")
app.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Dead root endpoint: returns a default message indicating there's no content.
@app.get("/")
def read_root():
    return {"message": "Dead root. No content available here."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
