@echo off
setlocal

rem Run from the add-on folder (the one containing blender_manifest.toml).
rem Set BLENDER_EXE to your blender.exe if it is not on PATH.
if "%BLENDER_EXE%"=="" set "BLENDER_EXE=blender"

cd /d "%~dp0"
if not exist blender_manifest.toml (
    echo blender_manifest.toml not found in %CD%
    exit /b 1
)

if not exist dist mkdir dist

rem Preferred: Blender's own builder (validates the manifest, honors [build] excludes).
where "%BLENDER_EXE%" >nul 2>nul
if %errorlevel%==0 (
    "%BLENDER_EXE%" --command extension build --output-dir dist
    exit /b %errorlevel%
)

rem Fallback: plain zip with Windows' built-in tar (forward-slash paths, Blender-safe).
echo Blender not found, falling back to tar.
tar -a -cf dist\simple_assist-1.0.0.zip ^
    --exclude=dist --exclude=__pycache__ --exclude=.git ^
    --exclude=launch.json --exclude=build.cmd *
exit /b %errorlevel%
