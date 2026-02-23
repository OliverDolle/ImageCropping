# Build script for Windows
# Usage: .\build_windows.ps1

Write-Host "Building Image Cropper for Windows..." -ForegroundColor Green

# Remove old build artifacts
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "main.spec") { Remove-Item "main.spec" }

# Build executable
pyinstaller --onefile --windowed --name "ImageCropper" --icon=NONE main.py

Write-Host "Build complete! Executable is in: dist/ImageCropper.exe" -ForegroundColor Green
