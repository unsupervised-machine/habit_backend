from fastapi import FastAPI
from routes import users, auth, habits, completions

app = FastAPI()


# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(habits.router, prefix="/habits", tags=["Habits"])
app.include_router(completions.router, prefix="/completions", tags=["Completions"])



@app.get("/")
async def root():
    return {"message": "Hello World"}