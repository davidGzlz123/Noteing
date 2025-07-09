@echo off

REM Backend
start "Backend" cmd /k "cd /d C:\Users\maxis\OneDrive\Documentos\DavidAgallas\Projects\Noting\noting && python manage.py runserver 0.0.0.0:8000"

REM Esperar 3 segundos antes de iniciar frontend
timeout /t 3 /nobreak > nul

REM Frontend (modificado para escuchar en 0.0.0.0:3000)
start "Frontend" cmd /k "cd /d C:\Users\maxis\OneDrive\Documentos\DavidAgallas\Projects\Noting\noting-frontend && set HOST=0.0.0.0&& set PORT=3000&& npm start"

REM Mantener esta ventana abierta
echo Backend y Frontend deberían estar corriendo en nuevas ventanas.
pause
