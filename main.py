from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api import api

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Main file only serves to run a 'main' file
# routes
app.include_router(router)
app.include_router(api)

# Add CORS middleware to prevent crosssitescripting
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
