



import tkinter as tk
import main
import GeminiAPI

from PIL import Image, ImageDraw, ImageTk

# Create the main window
root = tk.Tk()
root.title("Drawing App")
root.geometry("400x400")

# Create an Image object to store the drawing
canvas_width, canvas_height = 100, 100


# Create a Canvas widget
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack(pady=20)

global image, draw

image = Image.new("RGB", (canvas_width, canvas_height), "black")
draw = ImageDraw.Draw(image)

# Function to draw on the canvas
def paint(event):
    global image, draw
    x1, y1 = event.x - 2, event.y - 2
    x2, y2 = event.x + 2, event.y + 2
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
    draw.ellipse([x1, y1, x2, y2], fill="white")  # Draw on the Image object

# Bind the mouse motion to the paint function
canvas.bind("<B1-Motion>", paint)

# Function to save the image
def save_image():
    global image, draw
    filelocation = r"C:\Users\antony.irudayaraj\Desktop\VRTextEntry\Character_Images\drawing.jpg"

    image.save(filelocation)
    print("Image saved as drawing.png")
    GeminiAPI.process(filelocation)
    #main.process(filelocation)

# Function to clear the canvas
def clear_canvas():
    global image, draw
    canvas.delete("all")  # Clear the canvas

    image = Image.new('RGB', (canvas_width, canvas_height), color='black')
    draw = ImageDraw.Draw(image)
    print("Canvas cleared")

# Create a button to save the drawing
save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack(side=tk.LEFT, padx=10)

# Create a button to clear the canvas
clear_button = tk.Button(root, text="Clear Canvas", command=clear_canvas)
clear_button.pack(side=tk.LEFT, padx=10)

# Run the Tkinter main loop
root.mainloop()
