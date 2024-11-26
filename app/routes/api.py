from fastapi import Depends, APIRouter, Request, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from app.controllers.authentication import registerform, addregister, get_current_user, getrole, sessions, require_role
import sqlite3
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

api = APIRouter()

# Connect to SQLite database
conn = sqlite3.connect('./database/access.db', check_same_thread=False)

# List of database commands


def rows_to_dict(rows, columns):
    """Convert rows from the database to a list of dictionaries."""
    return [{column: value for column, value in zip(columns, row)} for row in rows]


# List of api's

@api.get("/api/onderzoeken")
async def onderzoeken(request: Request):

    # Permission check
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    require_role(session_id, required_role="Ervaringsdeskundige")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Onderzoeken WHERE actiefonderzoek =   1")
    rows = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    onderzoeken_data = rows_to_dict(rows, columns)

    return {"onderzoeken": onderzoeken_data}


@api.get("/api/onderzoeken/inactive")
async def get_inactive_onderzoeken(request: Request):

    # Permission Check
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    require_role(session_id, required_role="Beheerder")

    # Data grabbing/ manipulation
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Onderzoeken WHERE actiefonderzoek =   0")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    inactive_onderzoeken_data = rows_to_dict(rows, columns)

    return {"inactive_onderzoeken": inactive_onderzoeken_data}


@api.post("/api/onderzoeken/accept/{onderzoek_id}")
async def accept_onderzoek(onderzoek_id: int, request: Request):
    # Permission Check
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    require_role(session_id, required_role="Beheerder")

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Onderzoeken SET actiefonderzoek = 1 WHERE id = ?", (onderzoek_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Onderzoek niet gevonden")
    return {"status": "success", "message": "Onderzoek accepted successfully."}


@api.delete("/api/onderzoeken/delete/{onderzoek_id}")
async def delete_onderzoek(onderzoek_id: int, request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    require_role(session_id, required_role="Beheerder")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM Onderzoeken WHERE id = ?", (onderzoek_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Onderzoek niet gevonden")
    return {"status": "success", "message": "Onderzoek deleted successfully."}


@api.post("/api/onderzoeken/accept/{onderzoek_id}")
async def accept_onderzoek(onderzoek_id: int, request: Request):
    # Permission check
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    require_role(session_id, required_role="Ervaringsdeskundige")

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Onderzoeken SET actiefonderzoek = 1 WHERE id = ?", (onderzoek_id,))
    conn.commit()
    return {"status": "success", "message": "Onderzoek accepted successfully."}


@api.delete("/api/onderzoeken/delete/{onderzoek_id}")
async def delete_onderzoek(onderzoek_id: int, request: Request):
    # Permission check
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    require_role(session_id, required_role="Ervaringsdeskundige")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM Onderzoeken WHERE id = ?", (onderzoek_id,))
    conn.commit()
    return {"status": "success", "message": "Onderzoek deleted successfully."}


@api.get("/api/onderzoeken/{onderzoekid}")
async def onderzoeken(onderzoekid: int, request: Request):
    # Permission check
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    require_role(session_id, required_role="Ervaringsdeskundige")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Onderzoeken WHERE id = ?", (onderzoekid,))
    rows = cursor.fetchall()

    if rows:
        columns = [column[0] for column in cursor.description]
        onderzoeken_data = rows_to_dict(rows, columns)
        return {"onderzoeken": onderzoeken_data}
    else:
        return {"Error": "Onderzoek niet gevonden"}


# route for more info in popup modal
@api.get("/api/onderzoeken/details/{onderzoek_id}")
async def get_onderzoek_details(onderzoek_id: int, request: Request):
    # Permission check
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    require_role(session_id, required_role="Ervaringsdeskundige")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Onderzoeken WHERE id = ?", (onderzoek_id,))
    rows = cursor.fetchall()

    if rows:
        columns = [column[0] for column in cursor.description]
        onderzoeken_data = rows_to_dict(rows, columns)
        # Check if 'Met_beloning' is  1 and change it to 'ja'
        if onderzoeken_data[0]['Met_beloning'] == 1:
            onderzoeken_data[0]['Met_beloning'] = 'ja'
        else:
            onderzoeken_data[0]['Met_beloning'] = 'Nee'
            onderzoeken_data[0]['Beloning'] = 'N.V.T'
        return onderzoeken_data[0]
    else:
        raise HTTPException(status_code=404, detail="Onderzoek niet gevonden")

# route for applying for a onderzoek


@api.get("/api/onderzoeken/apply/{onderzoek_id}")
async def onderzoek_apply(onderzoek_id: int, request: Request):
    session_id = request.cookies.get("session_id")
    require_role(session_id, required_role="Ervaringsdeskundige")

    user_id = get_current_user(session_id=session_id)
    userid = str(user_id)
    cursor = conn.cursor()
    checkifalreadyaccepted = cursor.execute(
        "SELECT id FROM onderzoek WHERE gebruiker_id = ? AND onderzoek_id = ?", [userid, onderzoek_id])
    alreadyaccepted = checkifalreadyaccepted.fetchone()
    if alreadyaccepted == None:
        checkindatabase = cursor.execute(
            "SELECT id FROM aanvraag_deelname WHERE aanvrager_id = ? AND onderzoek_id = ?", [userid, onderzoek_id])
        alreadyrequested = checkindatabase.fetchone()
        if alreadyrequested == None:
            cursor.execute("INSERT INTO aanvraag_deelname (aanvrager_id, onderzoek_id) VALUES (?,?)", [
                           userid, onderzoek_id])
            conn.commit()
            cursor.close()
            return {"status": "success"}
        else:
            raise Exception
    else:
        raise Exception


@api.get("/api/gebruikers")
async def gebruikers(request: Request):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gebruikers")
    gebruikers = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    gebruikers_data = rows_to_dict(gebruikers, columns)

    return {"gebruikers": gebruikers_data}


# Gebruikers informatie ophalen op id
@api.get("/api/gebruikers/{gebruiker_id}")
async def gebruiker_details(request: Request, gebruiker_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gebruikers WHERE id = ?", (gebruiker_id,))
    gebruiker = cursor.fetchone()

    if not gebruiker:
        return {"error": "De gebruiker is niet gevonden!"}

    columns = [column[0] for column in cursor.description]
    gebruiker_data = rows_to_dict([gebruiker], columns)[0]

    return {"gebruiker": gebruiker_data}


# Gebruikers bewerken op id
@api.post("/api/gebruikers/{gebruiker_id}/edit")
async def update_gebruiker(request: Request, gebruiker_id: int, updated_gebruiker_data: dict):
    cursor = conn.cursor()

    gebruikersnaam = updated_gebruiker_data.get("gebruikersnaam")
    voornaam = updated_gebruiker_data.get("voornaam")
    achternaam = updated_gebruiker_data.get("achternaam")
    email = updated_gebruiker_data.get("email")
    gender = updated_gebruiker_data.get("gender")
    geboortedatum = updated_gebruiker_data.get("geboortedatum")
    postcode = updated_gebruiker_data.get("postcode")
    adres = updated_gebruiker_data.get("adres")
    toevoegingadres = updated_gebruiker_data.get("toevoegingadres")
    telefoonnummer = updated_gebruiker_data.get("telefoonnummer")

    rol_istoezichthouder = updated_gebruiker_data.get("rol_istoezichthouder", False)
    rol_isadmin = updated_gebruiker_data.get("rol_isadmin", False)
    rol_iservaringsdeskundige = updated_gebruiker_data.get("rol_iservaringsdeskundige", False)
    rol_isbeheerder = updated_gebruiker_data.get("rol_isbeheerder", False)

    cursor.execute(""" 
    UPDATE gebruikers SET 
        gebruikersnaam = ?, 
        voornaam = ?, 
        achternaam = ?,
        email = ?,
        gender = ?,
        geboortedatum = ?,
        postcode = ?,
        adres = ?,
        toevoegingadres = ?,
        telefoonnummer = ?,
        istoezichthouder = ?, 
        isadmin = ?, 
        iservaringsdeskundige = ?,
        isbeheerder = ?
         WHERE id = ?""", (gebruikersnaam, voornaam, achternaam, email,
                           gender, geboortedatum, postcode, adres, toevoegingadres,
                           telefoonnummer,
                           rol_istoezichthouder, rol_isadmin, rol_iservaringsdeskundige, rol_isbeheerder, gebruiker_id))

    conn.commit()
    return {"message": "Gegevens succesvol bijgewerkt!"}







# Route for making post requests to insert a onderzoek
# Define the Pydantic model for the onderzoek data
class Onderzoek(BaseModel):
    Titel: str
    Beschrijving: str
    Datum_vanaf: str
    Datum_tot: str
    Type_onderzoek: str
    Locatie: str
    Met_beloning: bool
    Beloning: Optional[str] = None
    Doelgroep_leeftijd_van: int
    Doelgroep_leeftijd_tot: int
    Doelgroep_beperking: Optional[str] = "None"
    Status: str

# Function to verify the API key


def verify_api_key(api_key: str = Depends(APIKeyHeader(name="X-API-KEY"))):

    def fetch_valid_api_keys(cursor):
        cursor.execute("SELECT apikey FROM organisaties")
        valid_api_keys = [row[0] for row in cursor.fetchall()]
        return valid_api_keys

    cursor = conn.cursor()
    valid_api_keys = fetch_valid_api_keys(cursor)

    if api_key not in valid_api_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key


@api.post("/api/onderzoeken/add")
async def add_onderzoek(onderzoek: Onderzoek, api_key: str = Depends(verify_api_key)):
    try:
        cursor = conn.cursor()

        # Convert boolean to int for database compatibility
        met_beloning_int = 1 if onderzoek.Met_beloning else 0

        default_actiefonderzoek = 0

        # Insert the data into the database
        cursor.execute("""
            INSERT INTO Onderzoeken (
                Titel, Beschrijving, Datum_vanaf, Datum_tot, 
                Type_onderzoek, Locatie, Met_beloning, Beloning, 
                Doelgroep_leeftijd_van, Doelgroep_leeftijd_tot, 
                Doelgroep_beperking, Status, actiefonderzoek
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            onderzoek.Titel, onderzoek.Beschrijving, onderzoek.Datum_vanaf, onderzoek.Datum_tot,
            onderzoek.Type_onderzoek, onderzoek.Locatie, met_beloning_int, onderzoek.Beloning,
            onderzoek.Doelgroep_leeftijd_van, onderzoek.Doelgroep_leeftijd_tot,
            onderzoek.Doelgroep_beperking, onderzoek.Status, default_actiefonderzoek
        ))

        conn.commit()
        return {"status": "success", "message": "Onderzoek added successfully."}
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api.get("/api/live_updates/users")
async def get_last_users(request: Request):
    session_id = request.cookies.get("session_id")
    require_role(session_id, required_role="Admin")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gebruikers ORDER BY id DESC LIMIT 3")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    last_users = rows_to_dict(rows, columns)
    return {"last_users": last_users}

@api.get("/api/live_updates/research_registrations")
async def get_last_research_registrations(request: Request):
    session_id = request.cookies.get("session_id")
    require_role(session_id, required_role="Admin")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM aanvraag_deelname ORDER BY id DESC LIMIT 3")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    last_research_registrations = rows_to_dict(rows, columns)
    return {"last_research_registrations": last_research_registrations}

@api.get("/api/live_updates/research_requests")
async def get_last_research_requests(request: Request):
    session_id = request.cookies.get("session_id")
    require_role(session_id, required_role="Admin")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM onderzoeken ORDER BY id DESC LIMIT 3")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    last_research_requests = rows_to_dict(rows, columns)
    return {"last_research_requests": last_research_requests}