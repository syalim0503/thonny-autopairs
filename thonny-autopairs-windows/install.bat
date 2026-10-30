@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

rem Thonny 괄호/따옴표 자동완성 플러그인 설치 (Windows)
rem Thonny에 들어 있는 python.exe로 install_helper.py를 실행해서
rem 그 Thonny가 쓰는 플러그인 폴더에 autopairs.py를 복사합니다.

set "THONNY_PY="
if exist "%LOCALAPPDATA%\Programs\Thonny\python.exe" set "THONNY_PY=%LOCALAPPDATA%\Programs\Thonny\python.exe"
if not defined THONNY_PY if exist "%ProgramFiles%\Thonny\python.exe" set "THONNY_PY=%ProgramFiles%\Thonny\python.exe"
if not defined THONNY_PY if exist "%ProgramFiles(x86)%\Thonny\python.exe" set "THONNY_PY=%ProgramFiles(x86)%\Thonny\python.exe"
if defined THONNY_PY goto install

echo Thonny 설치 폴더를 찾지 못했습니다.
echo Thonny 폴더 경로를 붙여넣고 Enter를 누르세요.
echo   (Thonny 바로가기 우클릭 - 파일 위치 열기 로 찾을 수 있습니다)
set "THONNY_DIR="
set /p "THONNY_DIR=경로: "
if not defined THONNY_DIR goto not_found
set "THONNY_DIR=%THONNY_DIR:"=%"
set "THONNY_PY=%THONNY_DIR%\python.exe"
if exist "%THONNY_PY%" goto install

:not_found
echo.
echo 그 폴더에서 python.exe를 찾지 못했습니다. 설치를 취소합니다.
pause
exit /b 1

:install
"%THONNY_PY%" -I "%~dp0install_helper.py"
if errorlevel 1 goto failed

echo.
echo Thonny를 껐다가 다시 열면 적용됩니다.
pause
exit /b 0

:failed
echo.
echo 설치에 실패했습니다. 위의 오류 메시지를 확인하세요.
pause
exit /b 1
