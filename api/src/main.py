from src.subjects.views import router as subjects_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(subjects_router)
