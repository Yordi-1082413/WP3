CREATE TABLE IF NOT EXISTS gebruikers (
  id INTEGER PRIMARY KEY,
  gebruikersnaam VARCHAR(50) UNIQUE,
  password VARCHAR(255),
  voornaam VARCHAR(50),
  tussenvoegsel VARCHAR(50),
  achternaam VARCHAR(50),
  email VARCHAR(100) UNIQUE,
  geboortedatum DATE,
  gender TEXT CHECK(gender IN ('man', 'vrouw', 'anders')),
  postcode VARCHAR(10),
  adres VARCHAR(255),
  toevoegingadres VARCHAR(100),
  telefoonnummer VARCHAR(15),
  toezichthouder BOOLEAN,
  ervaringsdeskundige_id INT,
  rolen_id INT,
  FOREIGN KEY (rolen_id) REFERENCES rollen(id)
  FOREIGN KEY (ervaringsdeskundige_id) REFERENCES ervaringsdeskundige(id)
);

CREATE TABLE if not exists rollen (
  id INTEGER PRIMARY KEY,
  beschrijving VARCHAR(255)
);

CREATE TABlE if not exists aanvraag_ervaringsdeskundige (
	id INTEGER PRIMARY KEY,
	aanvrager_id INTEGER,
	FOREIGN KEY (aanvrager_id) REFERENCES gebruikers(id)
);

CREATE TABlE if not exists aanvraag_toezichthouder (
	id INTEGER PRIMARY KEY,
	aanvrager_id INTEGER,
	FOREIGN KEY (aanvrager_id) REFERENCES gebruikers(id)
);

CREATE TABLE IF NOT EXISTS onderzoek (
  id INTEGER PRIMARY KEY,
  gebruiker_id INTEGER,
  onderzoeken_id INTEGER,
  FOREIGN KEY (onderzoeken_id) REFERENCES Onderzoeken(id)
  FOREIGN KEY (gebruiker_id) REFERENCES gebruikers(id)
);

CREATE TABLE if not exists Onderzoeken (
	id INTEGER PRIMARY KEY,
    Titel TEXT,
    Status TEXT,
    Beschikbaar BOOLEAN,
    Beschrijving TEXT,
    Datum_vanaf DATE,
    Datum_tot DATE,
    Type_onderzoek TEXT,
    Locatie TEXT,
    Met_beloning BOOLEAN,
    Beloning TEXT,
    Doelgroep_leeftijd_van INT,
    Doelgroep_leeftijd_tot INT,
    Doelgroep_beperking TEXT,
	actiefonderzoek BOOLEAN
);

CREATE TABlE if not exists aanvraag_deelname (
	id INTEGER PRIMARY KEY,
	aanvrager_id INTEGER,
	onderzoek_id TEXT,
	goedkeuringdeelname BOOLEAN,
	FOREIGN KEY (onderzoek_id) REFERENCES onderzoeken(id),
	FOREIGN KEY (aanvrager_id) REFERENCES gebruikers(id)
);

CREATE TABLE IF NOT EXISTS beperking (
  id INTEGER PRIMARY KEY,
  beperkingen_id INTEGER,
  gebruiker_id INTEGER,
  FOREIGN KEY (beperkingen_id) REFERENCES beperkingen(id),
  FOREIGN KEY (gebruiker_id) REFERENCES gebruikers(id)
);

CREATE TABLE IF NOT EXISTS beperkingen (
  id INTEGER PRIMARY KEY,
  beperking TEXT
);

CREATE TABLE IF NOT EXISTS toezichthouder (
  id INTEGER PRIMARY KEY,
  ervaringsdeskundige_id INTEGER,
  gebruiker_id INTEGER,
  FOREIGN KEY (gebruiker_id) REFERENCES gebruikers(id)
  FOREIGN KEY (ervaringsdeskundige_id) REFERENCES ervaringsdeskundige(id)
);

CREATE TABLE IF NOT EXISTS ervaringsdeskundige (
  id INTEGER PRIMARY KEY,
  gebruiker_id INTEGER,
  FOREIGN KEY (gebruiker_id) REFERENCES gebruikers(id)
);

CREATE TABLE if not exists organisaties (
	id INTEGER PRIMARY KEY,
    Naam TEXT,
    Type TEXT CHECK(Type IN ('Commercieel', 'non-profit')),
    Website TEXT,
    Beschrijving TEXT,
    Contactpersoon TEXT,
    Email TEXT,
    Telefoonnummer TEXT,
    Overige_details TEXT,
	apikey INT
);
