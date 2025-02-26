from fastapi import FastAPI
from routes import users, auth

app = FastAPI()


# Include routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])



@app.get("/")
async def root():
    return {"message": "Hello World"}