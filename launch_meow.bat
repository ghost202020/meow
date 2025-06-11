@echo off
REM MEOW File Format Launcher
REM Usage: Run this batch file to launch the GUI, or drag a .meow file onto it

if "%1"=="" (
    echo Starting MEOW GUI...
    python meow_gui.py
) else (
    if /I "%~x1"==".meow" (
        echo Opening %1 in MEOW Viewer...
        python meow_viewer.py "%1"
    ) else (
        echo Error: File must have .meow extension
        echo Usage: Drag a .meow file onto this launcher or run without arguments for GUI
        pause
    )
)
