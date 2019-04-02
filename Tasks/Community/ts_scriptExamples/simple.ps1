param(
   [string] $build
)

Write-Host "Hello, World!"

Write-Host "[ERROR] Powershell Error"
Write-Host "[CRITICAL] Powershell Critical"
Write-Host "[DEBUG] Powershell Debug"
Write-Host "[INFO] Powershell Info"
Write-Host "[WARNING] Powershell Warning"
Write-Host "[verified] Powershell OK"

Write-Host "Velocity API: $env:VELOCITY_PARAM_VELOCITY_API_ROOT"
Write-Host "Build argument is: $build"
Write-Host "Finished: PASSED"

