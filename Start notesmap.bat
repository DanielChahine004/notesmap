@echo off
rem Double-click to open your notes as a live map (Windows).
rem The first run downloads what it needs (a few minutes); later runs start at once.
rem Everything it downloads stays in this folder's .notesmap and .venv folders.
setlocal
cd /d "%~dp0"
title notesmap - close this window to stop the map

set "UV=uv"
where uv >nul 2>nul
if errorlevel 1 set "UV=%~dp0.notesmap\uv\uv.exe"
if not exist "%UV%" if not "%UV%"=="uv" (
    echo Setting up notesmap for the first time. This needs the internet and takes a few minutes.
    echo.
    powershell -NoProfile -ExecutionPolicy Bypass -Command "$env:UV_UNMANAGED_INSTALL='%~dp0.notesmap\uv'; irm https://astral.sh/uv/install.ps1 | iex"
    if not exist "%UV%" goto failed
)

echo Your notes are in the "notes" folder: edit notes\main.tex and the map updates as you save.
start "" explorer "%~dp0notes"
echo The map opens in your browser. Keep this window open while you use it; close it to stop.
echo.
"%UV%" run --no-dev --frozen notesmap serve --map
if errorlevel 1 goto failed
exit /b 0

:failed
echo.
echo Something went wrong (see the messages above). Press any key to close.
pause >nul
exit /b 1
