@echo off
echo Creating MEOW file association for Windows...
echo This will allow .meow files to open in any image viewer

REM Associate .meow extension with image viewers
echo Associating .meow with default image viewer...

REM For Windows Photos app
assoc .meow=PhotosApp.Image

REM Add PNG content type to registry (makes it work with image viewers)
reg add "HKEY_CLASSES_ROOT\.meow" /ve /d "PNGfile" /f
reg add "HKEY_CLASSES_ROOT\.meow" /v "Content Type" /d "image/png" /f
reg add "HKEY_CLASSES_ROOT\.meow" /v "PerceivedType" /d "image" /f

echo.
echo ✅ MEOW file association complete!
echo 📱 .meow files will now open in image viewers
echo 🖼️ They appear as PNG images but contain hidden MEOW data
echo.
echo To test: Double-click any .meow file in Windows Explorer
echo.
pause
