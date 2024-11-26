import datetime
from fastapi import Form, HTTPException, Request, APIRouter, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4
import sqlite3
from typing import List
from typing import Optional

from pydantic import BaseModel

from app.controllers.authentication import registerform, addregister, get_current_user, getrole, gotorolepage, sessions
from app.controllers.expert import insertrequestexpert, getexpertrequestpage
from app.controllers.authentication import registerform, addregister, get_current_user, getrole, gotorolepage, sessions, require_role
from app.controllers.authorizer import gotoreviewexpertrequests, getallexpertsrequestpage, deleterequestexpert, updateusertoexpert, getallexpertresearchregistrationspage, getallresearchregistrations, deleteresearchregristration, insertrequestexpertregristration

from app.controllers.admindash import (get_total_users, get_total_user_requests, get_total_research_registrations, get_total_research_requests)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Connect to SQLite database
conn = sqlite3.connect('./database/access.db', check_same_thread=False)


@router.get("/")
@router.get("/home", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

# Login system


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Register


@router.get('/register')
def register(request: Request):
    return registerform(request)


@router.post('/newregister')
def newregister(username: str = Form(...), password: str = Form(...), firstname: str = Form(...), sex: str = Form(...), infex: str = Form(None), lastname: str = Form(...), email: str = Form(...), dateofbirth: datetime.date = Form(...), postalcode: str = Form(...), addres: str = Form(...), addaddres: str = Form(None), phonenumber: str = Form(...)):
    return addregister(username, password, firstname, sex, infex, lastname, email, dateofbirth, postalcode, addres, addaddres, phonenumber)


@router.post("/token")
async def login_for_access_token(response: JSONResponse, username: str = Form(...), password: str = Form(...)):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM gebruikers WHERE gebruikersnaam = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Verkeerd wachtwoord of gebruikersnaam",
            headers={"WWW-Authenticate": "Bearer"},
        )

    session_id = str(uuid4())
    user_id = user[0]
    sessions[session_id] = {"user_id": user_id}
    response = RedirectResponse(
        url='/torolepage', status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_id", value=session_id)
    return response


@router.get('/torolepage')
def torolepage(request: Request):
    return gotorolepage(request)

# expertrequest


@router.get('/requestexpert')
def requestexpert(request: Request):
    return insertrequestexpert(request)


@router.get('/routes/getrequestfromexpert')
def getrequestfromexpert(request: Request):
    return getexpertrequestpage(request)

# authorizer


@router.get('/reviewexpertrequests')
def reviewexpertrequests(request: Request):
    return getallexpertsrequestpage(request)


@router.get('/routes/getrequestfromexperts')
def getrequestfromexperts(request: Request):
    return gotoreviewexpertrequests(request)


@router.get('/declinerequestexpert/{aanvrager_id}')
def declinerequestexpert(aanvrager_id: int):
    return deleterequestexpert(aanvrager_id)


@router.get('/acceptrequestexpert/{aanvrager_id}')
def acceptrequestexpert(aanvrager_id: int):
    return updateusertoexpert(aanvrager_id)


@router.get('/getallexpertresearchregistrations')
def getallexpertresearchregistrations(request: Request):
    return getallexpertresearchregistrationspage(request)


@router.get('/routes/getresearchregistrations')
def getresearchregistrations(request: Request):
    return getallresearchregistrations(request)


@router.get('/declineresearchregristration/{aanvrager_id}/{onderzoek_id}')
def declineresearchregristration(aanvrager_id: int, onderzoek_id: int):
    return deleteresearchregristration(aanvrager_id, onderzoek_id)


@router.get('/acceptrequestexpertregristration/{aanvrager_id}/{onderzoek_id}')
def acceptrequestexpertregristration(aanvrager_id: int, onderzoek_id: int):
    return insertrequestexpertregristration(aanvrager_id, onderzoek_id)

# Company requests


@router.get('/reviewcompanyrequests')
def pagecompanyrequests(request: Request):
    return templates.TemplateResponse("reviewcompanyrequests.html", {"request": request})


# Dashboard for ervaringsdeskundige
@router.get("/dash")
async def dash_redirect(request: Request):
    return RedirectResponse(url="/dashboard", status_code=308)


@router.get("/dashboard", response_class=HTMLResponse)
async def user_dashboard(request: Request):
    return templates.TemplateResponse("userdash.html", {"request": request})


# Logout route
@router.get("/logout")
async def user_logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")

    if session_id in sessions:
        # Remove all session data from the sessions dictionary
        sessions.pop(session_id)

    # Clear the session_id cookie
    response.delete_cookie(key="session_id")

    return RedirectResponse(url="/login", status_code=302)


@router.get("/dash/1")
async def user_dashboard(request: Request):
    return templates.TemplateResponse("onderzoekinfo.html", {"request": request})


@router.get("/gebruikers")
async def gebruiker_lijst(request: Request):
    return templates.TemplateResponse("gebruiker_lijst.html", {"request": request})


@router.get("/gebruikers/{gebruiker_id}")
async def gebruiker_details(request: Request, gebruiker_id: int):
    return templates.TemplateResponse("user_details.html", {"request": request, "gebruiker_id": gebruiker_id})


@router.get("/gebruikers/{gebruiker_id}/edit")
async def edit_gebruiker(request: Request, gebruiker_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gebruikers WHERE id = ?", (gebruiker_id,))
    gebruiker = cursor.fetchone()

    if not gebruiker:
        raise HTTPException(
            status_code=404, detail="Fout: Gebruiker niet gevonden")

    columns = [column[0] for column in cursor.description]
    gebruiker_data = dict(zip(columns, gebruiker))

    return templates.TemplateResponse("edit_user.html", {"request": request, "gebruiker": gebruiker_data})


@router.get("/admin")
async def admin_dashboard(request: Request):
    # Permission check
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    require_role(session_id, required_role="Admin")

    total_users = get_total_users()
    total_user_requests = get_total_user_requests()
    total_research_registrations = get_total_research_registrations()
    total_research_requests = get_total_research_requests()

    return templates.TemplateResponse("admindash.html", {"request": request, "total_users":total_users,
                                                         "total_user_requests":total_user_requests,
                                                         "total_research_registrations": total_research_registrations,
                                                         "total_research_requests":total_research_requests})

