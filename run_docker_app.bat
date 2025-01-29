@echo on

:: Navigate to the Xming directory and run Xming
cd .\Xming\
start .\Xming.exe -ac

:: Go back to the Dockerfile directory and build the Docker image
cd ..
docker build --tag pokemon .

:: Fetch the current host's IPv4 address and set the DISPLAY environment variable
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr "IPv4 Address"') do (
    for /f "tokens=* delims= " %%j in ("%%i") do set IP=%%j
)

set DISPLAY=%IP%:0.0

:: Display the resolved IP address for debugging
echo Host IP Address: %IP%
echo DISPLAY is set to %DISPLAY%

:: Run the Docker container
docker run -it --rm -e DISPLAY=%DISPLAY% --network="host" --name pokemon pokemon

:: Disable log visibility
echo off