from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
import sqlite3
from app.controllers.authentication import get_current_user

# stores session data
sessions = {}

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Connect to SQLite database
conn = sqlite3.connect('./database/access.db', check_same_thread=False)

def insertrequestexpert(request: Request):
    session_id = request.cookies.get("session_id")
    user_id = get_current_user(session_id=session_id)

    cursor = conn.cursor()
    cursor.execute("INSERT INTO aanvraag_ervaringsdeskundige (aanvrager_id) VALUES (?)", [user_id])
    conn.commit()
    cursor.close()
    return {"Added succesfully"}