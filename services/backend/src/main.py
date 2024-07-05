from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.register import register_tortoise  # NEW
from database.config import TORTOISE_ORM 

app = FastAPI()

# Add middleware to run a backend on different setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)

@app.get("/")
def home():
    return "Hello, World!"

