#!/bin/bash

#Snelle setup script voor Linux 


# Controleer of de virtuele omgeving al bestaat
if [ -d "venv" ]; then
    echo "Virtuele omgeving bestaat al. Activeren..."
    source venv/bin/activate
else
    echo "Virtuele omgeving bestaat niet. Aanmaken en activeren..."
    python -m venv venv
    source venv/bin/activate
    echo "Installeer de vereiste afhankelijkheden..."
    pip install -r requirements.txt
fi

# Start de FastAPI applicatie
echo "Starten van FastAPI applicatie..."
uvicorn main:app --reload

echo "FastAPI applicatie is gestart."
