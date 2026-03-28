from fastapi import FastAPI
from app import appRouter
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(appRouter.router)