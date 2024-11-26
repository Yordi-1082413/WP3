from fastapi import Form, HTTPException, Request, APIRouter, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4
import sqlite3

from app.controllers.authentication import get_current_user
from app.routes.api import rows_to_dict

# stores session dat
sessions = {}

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Connect to SQLite database
conn = sqlite3.connect('./database/access.db', check_same_thread=False)


def get_total_users():
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM gebruikers" )
    total_users = cursor.fetchone()[0]
    return total_users

def get_total_user_requests():
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM aanvraag_ervaringsdeskundige" )
    total_user_requests = cursor.fetchone()[0]
    return total_user_requests

def get_total_research_registrations():
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM aanvraag_deelname" )
    total_research_registrations = cursor.fetchone()[0]
    return total_research_registrations

def get_total_research_requests():
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM onderzoeken" )
    total_research_requests = cursor.fetchone()[0]
    return total_research_requests