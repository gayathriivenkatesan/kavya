@echo off
set "logFile=C:\Storage_Healthcheck_dashboard\Inputerror.log"
if exist "%logFile%" del "%logFile%"


powershell.exe C:\Storage_Healthcheck_dashboard\StorageDevice_Healthcheck_Dashboard.ps1 >> "%logFile%" 2>&1

if %errorlevel% neq 0 (
    echo An error occurred in the PowerShell script. Check the log file for details.
    goto :end
)