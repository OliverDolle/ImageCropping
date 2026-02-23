#!/bin/bash
# Build script for Linux
# Usage: bash build_linux.sh

echo "Building Image Cropper for Linux..."

# Remove old build artifacts
rm -rf dist build main.spec

# Build executable
pyinstaller --onefile --windowed --name "ImageCropper" main.py

echo "Build complete! Executable is in: dist/ImageCropper"
