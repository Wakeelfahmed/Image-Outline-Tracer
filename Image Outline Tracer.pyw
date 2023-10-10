import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import os

# Initialize global variables
original_image = None
processed_image = None
image_path = None  # Store the path of the selected image
dark_mode = False  # Track the mode (dark or white)
first_time = True
# Function to open a file dialog and select an image
def select_image():
    global original_image, processed_image, image_path, first_time
    image_path = filedialog.askopenfilename()
    if image_path:
        # Load the image using OpenCV
        original_image = cv2.imread(image_path)
        if original_image is not None:
            first_time = True
            processed_image = trace_outlines(original_image)
            apply_mode()
            display_processed_image()
            status_label.config(text="Image loaded and processed successfully.")
            save_button.config(state="normal")  # Enable the "Save Processed Image" button
            first_time = False
        else:
            status_label.config(text="Error: Unable to load the image.")
            save_button.config(state="disabled")  # Disable the "Save Processed Image" button
    else:
        status_label.config(text="No image selected.")
        save_button.config(state="disabled")  # Disable the "Save Processed Image" button

# Function to trace outlines using Canny edge detection
def trace_outlines(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 100, 200)
    traced_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return traced_image

# Function to apply the current mode to the processed image
def apply_mode():
    global processed_image, first_time
    if processed_image is not None:
        if dark_mode and first_time:
            #processed_image = cv2.bitwise_not(processed_image)  # Invert the processed image
            print("1st time part")
        elif dark_mode:
            processed_image = cv2.bitwise_not(processed_image)  # Invert the processed image
            print("if part")

        else:
            processed_image = cv2.bitwise_not(processed_image)  # Invert again to revert to the original
            print("else part")

# Function to display the processed image
def display_processed_image():
    global processed_image
    if processed_image is not None:
        processed_image_pil = Image.fromarray(processed_image)
        processed_image_pil = ImageTk.PhotoImage(processed_image_pil)
        
        # Clear any existing content on the canvas
        canvas.delete("all")
        
        # Calculate the center position for the image
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        image_width = processed_image_pil.width()
        image_height = processed_image_pil.height()
        
        x_center = (canvas_width - image_width) // 2
        y_center = (canvas_height - image_height) // 2
        
        # Display the image centered on the canvas
        canvas.create_image(x_center, y_center, anchor=tk.NW, image=processed_image_pil)
        
        # Update the canvas image
        canvas.image = processed_image_pil
        
        # Update scroll region to include the entire canvas
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

# Function to toggle between dark and white modes
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    apply_mode()
    display_processed_image()
    update_mode_buttons()  # Update the mode buttons to show the active mode

# Function to save the processed image
def save_image():
    global processed_image
    if processed_image is not None:
        file_extension = os.path.splitext(image_path)[1]  # Get the extension from the loaded image
        file_path = filedialog.asksaveasfilename(defaultextension=file_extension, filetypes=[(f"{file_extension.upper()} files", f"*{file_extension}"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, processed_image)  # Save the processed image
            status_label.config(text="Image saved successfully.")

# Function to update the mode buttons to show the active mode
def update_mode_buttons():
    if dark_mode:
        dark_mode_button.config(relief=tk.SUNKEN)
        white_mode_button.config(relief=tk.RAISED)
    else:
        dark_mode_button.config(relief=tk.RAISED)
        white_mode_button.config(relief=tk.SUNKEN)

# Create the GUI
root = tk.Tk()
root.title("Image Outline Tracer")
button_frame = tk.Frame(root)
button_frame.pack()
# Maximize the window
root.state('zoomed')

# Create a "Select Image" button
select_button = tk.Button(button_frame, text="Select Image", command=select_image)
select_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create a "Save Processed Image" button (initially disabled)
save_button = tk.Button(root, text="Save Processed Image", command=save_image, state="disabled")
save_button.pack()

# Create buttons to toggle between dark and white modes
dark_mode_button = tk.Button(button_frame, text="Dark Mode", command=toggle_dark_mode)
white_mode_button = tk.Button(button_frame, text="White Mode", command=toggle_dark_mode)
dark_mode_button.pack(side=tk.LEFT)
white_mode_button.pack(side=tk.LEFT)
white_mode_button.config(relief=tk.SUNKEN)

# Create a label to display status messages
status_label = tk.Label(root, text="")
status_label.pack()

# Create a canvas with scrollbars for displaying the processed image
canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)

# Add vertical scrollbar
v_scrollbar = tk.Scrollbar(canvas, orient=tk.VERTICAL)
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
v_scrollbar.config(command=canvas.yview)
canvas.config(yscrollcommand=v_scrollbar.set)

# Add horizontal scrollbar
h_scrollbar = tk.Scrollbar(canvas, orient=tk.HORIZONTAL)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
h_scrollbar.config(command=canvas.xview)
canvas.config(xscrollcommand=h_scrollbar.set)

# Bind canvas to configure event to update scroll region
canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox(tk.ALL)))

# Start the GUI main loop
root.mainloop()
