@echo off
chcp 65001 > nul
echo ========================================
echo Herramienta de Automatizacion Contable
echo ========================================
echo.
echo Archivos disponibles en data/input/
dir /b data\input\*.csv 2>nul
echo.
set /p archivo="Nombre del archivo (ej: transacciones.csv): "
echo.
cd src
py main.py %archivo%
echo.
echo ========================================
echo Proceso completado. Revisa data/output/
echo ========================================
pause