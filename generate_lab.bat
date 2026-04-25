@echo off
REM ============================================
REM PKT Lab Generator - Working Version
REM ============================================

echo.
echo ============================================
echo   PKT Lab Generator
echo ============================================
echo.

cd /d "%~dp0tracketpacin"

echo Available scenarios:
echo.
python main.py --list
echo.

set /p scenario=Enter scenario name: 

set /p seed=Enter seed number (or press Enter for random): 

if "%seed%"=="" (
    set seed=%RANDOM%
)

echo.
echo [1/3] Generating topology...
python main.py --scenario %scenario% --output temp_lab.xml --skip-pkt --seed %seed%

if errorlevel 1 (
    echo.
    echo ERROR: Failed to generate lab. Check scenario name.
    pause
    exit /b 1
)

echo [2/3] Fixing file structure...
python fix_pkt_v2.py temp_lab.xml temp_lab_fixed.xml

if errorlevel 1 (
    echo.
    echo ERROR: Failed to fix XML
    pause
    exit /b 1
)

echo [3/3] Converting to .pkt...
python ptexplorer.py -e temp_lab_fixed.xml "..\%scenario%_lab.pkt"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create .pkt file
    pause
    exit /b 1
)

REM Cleanup temp files
del temp_lab.xml temp_lab_fixed.xml 2>nul

echo.
echo ============================================
echo   SUCCESS!
echo ============================================
echo.
echo File saved to: %~dp0%scenario%_lab.pkt
echo.
echo Open this file in Cisco Packet Tracer!
echo.
pause
