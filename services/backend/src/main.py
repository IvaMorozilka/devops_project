from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.register import register_tortoise  # NEW
from database.config import TORTOISE_ORM 
from tortoise import Tortoise
import uvicorn

Tortoise.init_models(['database.models'], 'models')

from routes import users, todos

app = FastAPI()

# Add middleware to run a backend on different setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(todos.router)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True)

if __name__ == "__main__":
    uvicorn.run(app)
