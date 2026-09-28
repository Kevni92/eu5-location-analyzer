@echo off
setlocal

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%~dp0build_debug_gui.py" %*
  if errorlevel 1 goto :failed
  py -3 "%~dp0add_economy_pies.py" %*
) else (
  python "%~dp0build_debug_gui.py" %*
  if errorlevel 1 goto :failed
  python "%~dp0add_economy_pies.py" %*
)

if errorlevel 1 goto :failed

echo.
echo Build complete. The repository root now contains the generated Workshop-ready GUI override.
pause
exit /b 0

:failed
echo.
echo Build failed. See the error above.
pause
exit /b 1
