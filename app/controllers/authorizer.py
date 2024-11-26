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

def getallexpertsrequestpage(request: Request):
    return templates.TemplateResponse("reviewexpertrequests.html", {"request": request})

def gotoreviewexpertrequests(request: Request):
    cursor = conn.cursor()
    cursor.execute("SELECT aanvrager_id, gebruikersnaam, email, telefoonnummer FROM aanvraag_ervaringsdeskundige INNER JOIN gebruikers ON aanvraag_ervaringsdeskundige.aanvrager_id = gebruikers.id")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    requests_data = rows_to_dict(rows, columns)
    return {"requests": requests_data}

def deleterequestexpert(aanvrager_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM aanvraag_ervaringsdeskundige WHERE aanvrager_id=?", (aanvrager_id,))
    conn.commit()
    response = RedirectResponse(url='/reviewexpertrequests', status_code=status.HTTP_303_SEE_OTHER)
    return response

def updateusertoexpert(aanvrager_id: int):
    cursor = conn.cursor()
    cursor.execute("UPDATE gebruikers SET iservaringsdeskundige=? WHERE id=?", (True, aanvrager_id,))
    cursor.execute("DELETE FROM aanvraag_ervaringsdeskundige WHERE aanvrager_id=?", (aanvrager_id,))
    conn.commit()
    response = RedirectResponse(url='/reviewexpertrequests', status_code=status.HTTP_303_SEE_OTHER)
    return response

def getallexpertresearchregistrationspage(request: Request):
    return templates.TemplateResponse("reviewexpertresearchregistrations.html", {"request": request})

def getallresearchregistrations(request: Request):
    cursor = conn.cursor()
    cursor.execute("SELECT titel, onderzoek_id, type_onderzoek, aanvrager_id, gebruikersnaam, email, telefoonnummer FROM aanvraag_deelname INNER JOIN gebruikers ON aanvraag_deelname.aanvrager_id = gebruikers.id INNER JOIN onderzoeken ON aanvraag_deelname.onderzoek_id = onderzoeken.id")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    requests_data = rows_to_dict(rows, columns)
    return {"requests": requests_data}

def deleteresearchregristration(aanvrager_id: int, onderzoek_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM aanvraag_deelname WHERE aanvrager_id=? AND onderzoek_id=?", (aanvrager_id, onderzoek_id))
    conn.commit()
    response = RedirectResponse(url='/getallexpertresearchregistrations', status_code=status.HTTP_303_SEE_OTHER)
    return response

def insertrequestexpertregristration(aanvrager_id: int, onderzoek_id: int):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO onderzoek (gebruiker_id,onderzoek_id) VALUES (?,?)", [aanvrager_id,onderzoek_id])
    cursor.execute("DELETE FROM aanvraag_deelname WHERE aanvrager_id=? AND onderzoek_id=?", (aanvrager_id, onderzoek_id))
    conn.commit()
    response = RedirectResponse(url='/getallexpertresearchregistrations', status_code=status.HTTP_303_SEE_OTHER)
    return response
