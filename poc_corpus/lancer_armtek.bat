@echo off
cd /d %~dp0

echo === Étape 1/3 : Lancement de l'API FastAPI sur http://127.0.0.1:8000 ===
start cmd /k "uvicorn main:app --reload"

echo === Étape 2/3 : Serveur local pour l'interface utilisateur ===
start cmd /k "python -m http.server 9000"

timeout /t 3 > nul

echo === Étape 3/3 : Ouverture du navigateur ===
start http://127.0.0.1:9000/index.html

exit
