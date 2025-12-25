# Image Cropper

A simple Python GUI application for cropping and resizing images.

## Features

- Upload images (JPG, PNG, BMP, GIF)
- Interactive cropping with draggable rectangle
- Real-time preview of cropped area
- Scale adjustment (10% to 200%) with live preview
- Pixelated preview for small scaled images
- Save cropped images in various formats
- Real-time file size and dimension updates

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed
3. Install dependencies:
   ```
   pip install pillow
   ```
4. Run the application:
   ```
   python main.py
   ```

## Usage

### Image Upload

1. Click the "Upload Image" button
2. Select an image file from your computer (supported formats: JPG, JPEG, PNG, BMP, GIF)
3. The image will be displayed in the canvas

### Cropping

- A red rectangle appears on the image representing the crop area
- Drag the rectangle to move it
- Drag the bottom-right corner to resize it
- The pixel dimensions and file size update in real-time

### Scaling

- Use the scale slider (10% to 200%) to resize the cropped image
- The preview shows how the final image will look
- Small scaled images appear pixelated in the preview to show quality

### Saving

- Click "Save Cropped Image" to save the result
- Choose file name and format (JPEG, PNG, BMP, GIF)
- The saved image will be cropped and scaled as set

## Requirements

- Python 3.6+
- Pillow (PIL) library

## License

This project is open source. Feel free to use and modify.