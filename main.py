from fastapi import FastAPI
from routes import users

app = FastAPI()


# Include routes
app.include_router(users.router, prefix="/users", tags=["Users"])



@app.get("/")
async def root():
    return {"message": "Hello World"}