"""
BMI Calculator GUI Application

File: BMI_calculator.py
Folder: BMI_calculator
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from typing import Any

# --- Constants ---
LIGHT_YELLOW = '#FFFFE0'


# --- Functions ---
def calculate_bmi():
    """Calculates BMI and displays the result and category."""
    try:
        height_str = height_entry.get()
        weight_kg = int(weight_entry.get())

        if "," in height_str:
            height_str = height_str.replace(",", ".")

        height_cm = float(height_str)
        height_meters = height_cm / 100

        if height_meters <= 0 or weight_kg <= 0:
            result_label.config(
                text="Error: Height and weight must be positive numbers.",
                fg="red"
            )
            return

        bmi = weight_kg / (height_meters ** 2)
        rounded_bmi = round(bmi, 2)

        if rounded_bmi < 18.5:
            category = "Underweight"
            color = "deepskyblue"
        elif 18.5 <= rounded_bmi <= 24.9:
            category = "Normal weight"
            color = "green"
        elif 25.0 <= rounded_bmi <= 29.9:
            category = "Overweight"
            color = "darkorange"
        elif 30.0 <= rounded_bmi <= 34.9:
            category = "Obesity Class I"
            color = "salmon"
        elif 35.0 <= rounded_bmi <= 39.9:
            category = "Obesity Class II"
            color = "crimson"
        else:
            category = "Obesity Class III (severe)"
            color = "darkred"

        result_text = (
            f"Your BMI is: {rounded_bmi}\n"
            f"According to WHO classification, your BMI falls in the '{category}' category."
        )
        result_label.config(text=result_text, fg=color)

    except ValueError:
        result_label.config(
            text="Error: Please enter valid numbers for height and weight.",
            fg="red"
        )


def focus_to_weight(_event):
    """Moves focus from height entry to weight entry when Enter is pressed."""
    weight_entry.focus_set()


def trigger_calculate(_event):
    """Triggers BMI calculation when Enter is pressed in the weight entry."""
    calculate_bmi()


# --- Main window setup ---
window = tk.Tk()
window.title("BMI Calculator")
window_width = 700
window_height = 700
window.geometry(f"{window_width}x{window_height}")
window.resizable(False, False)
window.config(bg=LIGHT_YELLOW)

# --- Image loading ---
new_height = 300  # Default height if image fails to load
image_path = os.path.join(os.path.dirname(__file__), "BMI-chart.PNG")

try:
    img = Image.open(image_path)
    original_width, original_height = img.size

    max_image_width = window_width - 40
    max_image_height = 300

    if original_height > max_image_height:
        aspect_ratio = original_width / original_height
        new_height = max_image_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = original_width
        new_height = original_height

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    img_tk: Any = ImageTk.PhotoImage(img)

    center_x = (window_width - new_width) // 2
    image_label = tk.Label(window, image=img_tk, bg=LIGHT_YELLOW)
    image_label.image = img_tk
    image_label.place(x=center_x, y=0, width=new_width, height=new_height)

except FileNotFoundError:
    error_message = (
        "Image not found. Make sure 'BMI-chart.PNG' is in the same directory as the script."
    )
    image_label = tk.Label(
        window,
        text=error_message,
        fg="red",
        bg=LIGHT_YELLOW,
        wraplength=window_width - 40
    )
    image_label.place(x=20, y=0, relwidth=1, height=300)

except Exception as e:
    messagebox.showerror("Image Error", f"An error occurred while loading the image: {e}")

# --- Input section ---
input_frame = tk.Frame(window, bg=LIGHT_YELLOW)
input_frame_pady_top = new_height + 20
input_frame.pack(pady=(input_frame_pady_top, 10))

# --- Height input ---
height_label = tk.Label(
    input_frame,
    text="Height in centimeters (e.g., 175):",
    bg=LIGHT_YELLOW
)
height_label.pack()

height_entry = tk.Entry(input_frame, width=30)
height_entry.pack(pady=5)

# --- Weight input ---
weight_label = tk.Label(
    input_frame,
    text="Weight in kilograms (e.g., 70):",
    bg=LIGHT_YELLOW
)
weight_label.pack()

weight_entry = tk.Entry(input_frame, width=30)
weight_entry.pack(pady=5)

# --- Keyboard bindings ---
height_entry.bind("<Return>", focus_to_weight)
weight_entry.bind("<Return>", trigger_calculate)

# --- Calculate button ---
calculate_button = tk.Button(
    input_frame,
    text="Calculate BMI",
    command=calculate_bmi
)
calculate_button.pack(pady=15)

# --- Result display ---
result_label = tk.Label(
    window,
    text="",
    font=("Helvetica", 12, "bold"),
    bg=LIGHT_YELLOW
)
result_label.pack(pady=10)

# --- Start GUI loop ---
window.mainloop()
