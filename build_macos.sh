#!/bin/bash
# Build script for macOS
# Usage: bash build_macos.sh

echo "Building Image Cropper for macOS..."

# Remove old build artifacts
rm -rf dist build main.spec

# Build executable as an app bundle
pyinstaller --onefile --windowed --osx-bundle-identifier=com.imagecropper --name "ImageCropper" main.py

echo "Build complete! Application is in: dist/ImageCropper.app"
