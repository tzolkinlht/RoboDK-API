: IMPORTANT!!! setup.py gets overriden by a_rdk_set_version.py
: Update a_rdk_set_version.py if setup.py is changed

@echo off

::----------------------------------
:: Create Python venv
@echo ---------------
@echo Creating env..
CALL env.bat

::----------------------------------
:: ./tools
CD ..
:top

::----------------------------------
:: Clean previous build
@echo ---------------
@echo Cleaning last build...
if exist "build"           rmdir /S /Q "build"
if exist "dist"            rmdir /S /Q "dist"
if exist "robodk.egg-info" rmdir /S /Q "robodk.egg-info"
if exist "build_python2"   rmdir /S /Q "build_python2"

::----------------------------------
:: Strip type hints for Python 2
@echo ---------------
@echo Stripping type hints for Python 2 compatibility...
pause
cd tools
%VIRTUAL_ENV%\Scripts\python.exe python2.py
if errorlevel 1 (
   goto end
)
cd ..

cd build_python2

::----------------------------------
:: Test the install on Python 2
:: pip install . -I is not supported for Python 2 anymore
@REM @echo ---------------
@REM @echo Press a key to TEST the Python package
@REM pause
@REM C:\Python27\Scripts\pip install --upgrade pip
@REM C:\Python27\Scripts\pip uninstall robodk
@REM C:\Python27\Scripts\pip install . -I
@REM if errorlevel 1 (
@REM    goto end
@REM )


::----------------------------------
:: Build the package with wheel
@echo ---------------
@echo Press a key to BUILD the Python package
pause
%VIRTUAL_ENV%\Scripts\python.exe setup.py bdist_wheel
if errorlevel 1 (
   goto end
)


::----------------------------------
:: Test the install on Python 2
@echo ---------------
@echo Press a key to TEST the Python package (Python 2.7)
pause
FOR /R %%F IN (*.whl) DO (
   C:\Python27\Scripts\pip uninstall robodk
   C:\Python27\Scripts\pip install %%F
)
if errorlevel 1 (
   goto end
)


::----------------------------------
:: Upload the package to PyPi with twine (will ask for credentials)
@echo ---------------
@echo Press a key to UPLOAD to PyPi
pause
%VIRTUAL_ENV%\Scripts\twine upload dist/*

cd ..


::----------------------------------
:: Clean the build
@echo ---------------
@echo Press a key to clean the build
pause
if exist "build"           rmdir /S /Q "build"
if exist "dist"            rmdir /S /Q "dist"
if exist "robodk.egg-info" rmdir /S /Q "robodk.egg-info"
if exist "build_python2"   rmdir /S /Q "build_python2"


::----------------------------------
:: Offer to start over
:end
set choice=
set /p choice="Enter r to restart, anything else to exit: "
if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='r' goto top
cmd /k pause
