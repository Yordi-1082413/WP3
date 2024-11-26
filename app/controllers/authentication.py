from fastapi import Form, HTTPException, Request, APIRouter, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4
import sqlite3
from typing import List
from fastapi import Cookie, status, requests
from pydantic import BaseModel
# stores session data
sessions = {}

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Connect to SQLite database
conn = sqlite3.connect('./database/access.db', check_same_thread=False)


def registerform(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


def addregister(username, password, firstname, sex, infex, lastname, email, dateofbirth, postalcode, addres, addaddres, phonenumber):
    istoezichthouder = False
    iservaringsdeskundige = False
    isadmin = False
    isbeheerder = False
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gebruikers (gebruikersnaam, password, voornaam, tussenvoegsel, achternaam, email, geboortedatum, gender, postcode, adres, toevoegingadres, telefoonnummer, istoezichthouder, iservaringsdeskundige, isadmin, isbeheerder) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [
                   username, password, firstname, infex, lastname, email, dateofbirth, sex, postalcode, addres, addaddres, phonenumber, istoezichthouder, iservaringsdeskundige, isadmin, isbeheerder])
    conn.commit()
    cursor.close()
    response = RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)
    return response


def get_current_user(session_id: str = Cookie(None)):
    if session_id in sessions:
        return sessions[session_id]['user_id']
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


def getrole(request: Request):
    session_id = request.cookies.get("session_id")
    user_id = get_current_user(session_id=session_id)
    userid = str(user_id)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gebruikers WHERE id = ?", (userid))
    user_role = cursor.fetchone()

    if user_role[0] == 1:
        user_role_description = "Admin"
    else:
        user_role_description = "Ervaringsdeskundige"

    return user_role_description

def gotorolepage(request: Request):
    session_id = request.cookies.get("session_id")
    user_id = get_current_user(session_id=session_id)
    userid = str(user_id)
    
    cursor = conn.cursor()
    cursor.execute("SELECT iservaringsdeskundige, isadmin, isbeheerder FROM gebruikers WHERE id = ?", (userid, ))
    user_role = cursor.fetchone()
    cursor.close()

    print("Waarden van user_role:", user_role)
    #zorgt voor het sturen van paginas waneer je iets bent of niet iets bent
    #user_role[0] = isadmin en user_role[1] = iservaringsdeskundige user_role[2] = isbeheerder
    if user_role[0] == 1 and user_role[1] == 0 and user_role[2] == 0:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    elif user_role[0] == 0 and user_role[1] == 0 and user_role[2] == 0:
        return templates.TemplateResponse("aanvragingervaringsdeskundige.html", {"request": request})
    elif user_role[0] == 0 and user_role[1] == 0 and user_role[2] == 1:
        return templates.TemplateResponse("beheerderpagina.html", {"request": request})
    elif user_role[0] == 0 and user_role[1] == 1 and user_role[2] == 0:
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    else:
        return user_role

#Function to check user has the right permissions
def require_role(session_id: str, required_role: str) -> bool:
    if session_id not in sessions:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Niet ingelogd")
    
    user_id = sessions[session_id]['user_id']
    cursor = conn.cursor()
    cursor.execute("SELECT isBeheerder, iservaringsdeskundige, isadmin, istoezichthouder FROM gebruikers WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    role_list = {
        "Beheerder": user_data[0],
        "Ervaringsdeskundige": user_data[1],
        "Admin": user_data[2],
        "Toezichthouder": user_data[3]
    }
    
    if role_list[required_role] !=  1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Je hebt geen permissie voor deze pagina")
    
    return True
