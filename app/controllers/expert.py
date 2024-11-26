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

def getexpertrequestpage(request: Request):
    session_id = request.cookies.get("session_id")
    user_id = get_current_user(session_id=session_id)
    userid = str(user_id)

    cursor = conn.cursor()
    checkifexpert = cursor.execute("SELECT iservaringsdeskundige FROM gebruikers WHERE id = ?", (userid))
    isexpert = checkifexpert.fetchone()
    #isexpert[0] == 0 = if iservaringsdekunige is 0 in datanase
    if isexpert[0] == 0:
        cursor.execute("SELECT aanvrager_id FROM aanvraag_ervaringsdeskundige WHERE aanvrager_id = ?", (userid))
        expertrequest = cursor.fetchone()
        #if expertrequest == none = if aanvrager_id doesnt exist in aanvraag_ervaringsdeskundige table
        #request 0 stands for request page/ request 1 stand for already did request/ request 2 stands for request accepted
        if expertrequest == None:
            request = 0
        else:
            request = 1
        # Use the helper function to convert rows to dictionaries
        return {"requests": request}
    else:
        request = 2
        return {"requests": request}

def insertrequestexpert(request: Request):
    session_id = request.cookies.get("session_id")
    user_id = get_current_user(session_id=session_id)
    userid = str(user_id)

    cursor = conn.cursor()
    cursor.execute("INSERT INTO aanvraag_ervaringsdeskundige (aanvrager_id) VALUES (?)", [userid])
    conn.commit()
    cursor.close()
    return templates.TemplateResponse("aanvragingervaringsdeskundige.html", {"request": request})

def insertrequestresearch(request: Request, onderzoek_id: int):
    session_id = request.cookies.get("session_id")
    user_id = get_current_user(session_id=session_id)
    userid = str(user_id)
    cursor = conn.cursor()
    checkindatabase = cursor.execute("SELECT id FROM aanvraag_deelname WHERE aanvrager_id = ? AND onderzoek_id = ?", [userid, onderzoek_id])
    alreadyrequested = checkindatabase.fetchone()
    if alreadyrequested == None:
        cursor.execute("INSERT INTO aanvraag_deelname (aanvrager_id, onderzoek_id) VALUES (?,?)", [userid, onderzoek_id])
        conn.commit()
        cursor.close()
        return RedirectResponse(url="/dash", status_code=302)
    else: 
        return RedirectResponse(url="/dash", status_code=302)