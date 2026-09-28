@echo off
setlocal

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%~dp0build_debug_gui.py" %*
) else (
  python "%~dp0build_debug_gui.py" %*
)

if errorlevel 1 (
  echo.
  echo Build failed. See the error above.
  pause
  exit /b 1
)

echo.
echo Build complete. The repository root now contains the generated Workshop-ready GUI override.
pause
