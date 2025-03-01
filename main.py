from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, auth, habits, completions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://habit-frontend-five.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(habits.router, prefix="/habits", tags=["Habits"])
app.include_router(completions.router, prefix="/completions", tags=["Completions"])



@app.get("/")
async def root():
    return {"message": "Hello World"}