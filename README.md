# wp3-2024-NullNinjas

Hallo, hierbij ons project hier kan je via de homepagina inloggen op ons portaal, gebaseerd op jouw role wordt je automatisch naar de goede pagina gestuurd.
Daarom krijg je ook een andere ervaring per account, probeer alle accounts die onderaan dit bestand staan.
Je kan met Beheerder gebruikers accounts editen etc.
Met Admin kan je alles editen etc.
Met Ervaringsdeskundige kan je je aanmelden voor onderzoeken, daarna moet je wachten om goedgekeurd te worden door een Beheerder.


## Installatie
Voor linux doe 
```bash
   sudo chmod +x ./setup.sh
   ./setup.sh
```

Voor windows :

1. Clone deze repository naar je lokale machine.
   ```bash
   git clone https://github.com/Rac-Software-Development/wp2-2023-mvc-1c-racy.git
   cd wp3-2024-rest-1d1-nullninjas
   ```
2. Maak een virtuele omgeving en activeer deze.
```bash
python -m venv venv
venv\Scripts\activate
```

3. Installeer de vereiste afhankelijkheden.
```bash
pip install -r requirements.txt
```
4. Start de server, in VSCode kan je F5 indrukken voor een dev environment
anders gerbuik
```bash
uvicorn 'main:app' '--reload'
```

# Inloggen

- Admin:
-> **username:** hoi **password** hoi
- ervaringsdeskundige:
->  **username:** user **password** ww
- Beheerder/bedrijf:
-> **username:** beheerder **password** beheerder



# Api documentatie

Alle api routes kan je vinden door naar /docs route te gaan in de applicatie
localhost:8000/docs

Voor het bedrijfs api, bekijk de postman-bedrijf-post.json file, het is een postman file.


# ERD

Kijk erd.png

# Korte uitleg over zaken waarvan je wilt dat we deze extra aandacht geven - iets waarop je trots bent. 

De popup op de /dashboard pagina is gemaakt d.m.v JQuery voor extra animaties/fadeouts.
Het A4 design van de website vindt een goede manier om het bekend voor mensen te laten voelen.
