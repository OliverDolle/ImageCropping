from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import io

class ImageCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")
        self.upload_btn = Button(root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack()
        self.save_btn = Button(root, text="Save Cropped Image", command=self.save_image, state=DISABLED)
        self.save_btn.pack()
        self.scale_var = DoubleVar(value=100.0)
        self.scale_label = Label(root, text="Scale: 100%")
        self.scale_label.pack()
        self.scale_slider = Scale(root, from_=10, to=200, orient=HORIZONTAL, variable=self.scale_var, command=self.on_scale_change)
        self.scale_slider.pack()
        self.canvas = Canvas(root, width=800, height=600)
        self.canvas.pack()
        self.pixel_label = Label(root, text="Pixel Size: ")
        self.pixel_label.pack()
        self.file_label = Label(root, text="File Size: ")
        self.file_label.pack()
        self.image = None
        self.photo = None
        self.crop_rect = None
        self.dragging = False
        self.resize = False
        self.start_x = 0
        self.start_y = 0
        self.rect_x1 = 100
        self.rect_y1 = 100
        self.rect_x2 = 300
        self.rect_y2 = 300
        self.scale = 1
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def upload_image(self):
        file_path = filedialog.askopenfilename(initialdir=".", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image()
            self.draw_crop_rect()
            self.update_info()
            self.save_btn.config(state=NORMAL)

    def display_image(self):
        # Scale to fit canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 600
        img_width, img_height = self.image.size
        scale = min(canvas_width / img_width, canvas_height / img_height, 1)  # Don't upscale
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        resized = self.image.resize((new_width, new_height), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized)
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.scale = scale

    def draw_crop_rect(self):
        if self.crop_rect:
            self.canvas.delete(self.crop_rect)
        self.crop_rect = self.canvas.create_rectangle(self.rect_x1, self.rect_y1, self.rect_x2, self.rect_y2, outline="red", width=2)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        # Check if near bottom-right corner
        if abs(event.x - self.rect_x2) < 10 and abs(event.y - self.rect_y2) < 10:
            self.resize = True
        elif self.rect_x1 <= event.x <= self.rect_x2 and self.rect_y1 <= event.y <= self.rect_y2:
            self.dragging = True

    def on_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        if self.resize:
            self.rect_x2 = max(self.rect_x1 + 10, self.rect_x2 + dx)
            self.rect_y2 = max(self.rect_y1 + 10, self.rect_y2 + dy)
        elif self.dragging:
            self.rect_x1 += dx
            self.rect_y1 += dy
            self.rect_x2 += dx
            self.rect_y2 += dy
        self.start_x = event.x
        self.start_y = event.y
        self.draw_crop_rect()
        self.update_info()

    def on_release(self, event):
        self.dragging = False
        self.resize = False

    def on_scale_change(self, value):
        self.scale_label.config(text=f"Scale: {int(float(value))}%")
        self.update_info()

    def update_info(self):
        if not self.image:
            return
        scale_factor = self.scale_var.get() / 100.0
        # Pixel size: width x height of crop in original, scaled
        crop_width = int((self.rect_x2 - self.rect_x1) / self.scale * scale_factor)
        crop_height = int((self.rect_y2 - self.rect_y1) / self.scale * scale_factor)
        self.pixel_label.config(text=f"Pixel Size: {crop_width} x {crop_height}")
        # File size: crop the image, scale, and get size
        left = max(0, int(self.rect_x1 / self.scale))
        top = max(0, int(self.rect_y1 / self.scale))
        right = min(self.image.size[0], int(self.rect_x2 / self.scale))
        bottom = min(self.image.size[1], int(self.rect_y2 / self.scale))
        cropped = self.image.crop((left, top, right, bottom))
        if scale_factor != 1.0:
            new_width = int(cropped.size[0] * scale_factor)
            new_height = int(cropped.size[1] * scale_factor)
            cropped = cropped.resize((new_width, new_height), Image.LANCZOS)
        # Save to bytes
        buf = io.BytesIO()
        cropped.save(buf, format='JPEG')
        size_bytes = buf.tell()
        if size_bytes >= 1024*1024:
            size = size_bytes / (1024*1024)
            unit = "MB"
        else:
            size = size_bytes / 1024
            unit = "KB"
        self.file_label.config(text=f"File Size: {size:.2f} {unit}")

    def save_image(self):
        if not self.image:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp"), ("GIF", "*.gif")])
        if file_path:
            scale_factor = self.scale_var.get() / 100.0
            left = max(0, int(self.rect_x1 / self.scale))
            top = max(0, int(self.rect_y1 / self.scale))
            right = min(self.image.size[0], int(self.rect_x2 / self.scale))
            bottom = min(self.image.size[1], int(self.rect_y2 / self.scale))
            cropped = self.image.crop((left, top, right, bottom))
            if scale_factor != 1.0:
                new_width = int(cropped.size[0] * scale_factor)
                new_height = int(cropped.size[1] * scale_factor)
                cropped = cropped.resize((new_width, new_height), Image.LANCZOS)
            # Determine format from extension
            ext = file_path.split('.')[-1].lower()
            if ext == 'jpg':
                ext = 'JPEG'
            elif ext == 'png':
                ext = 'PNG'
            elif ext == 'bmp':
                ext = 'BMP'
            elif ext == 'gif':
                ext = 'GIF'
            else:
                ext = 'JPEG'
            cropped.save(file_path, ext)

if __name__ == "__main__":
    root = Tk()
    app = ImageCropper(root)
    root.mainloop()