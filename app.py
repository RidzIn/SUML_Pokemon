import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Tuple
from PIL import Image, ImageTk
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the ML model and tokenizer
def load_model(model_name: str) -> Tuple[BlipProcessor, BlipForConditionalGeneration]:
    """
    Loads a BLIP model and processor from the Hugging Face Hub.

    Args:
        model_name (str): The name of the model on Hugging Face Hub.
                          e.g., "Salesforce/blip-image-captioning-large", "RidzIn/Pokemon-Describer"

    Returns:
        Tuple[BlipProcessor, BlipForConditionalGeneration]:
            - processor: The BLIP processor for tokenizing images and text.
            - model: The BLIP model (for conditional generation).
    """
    processor = BlipProcessor.from_pretrained(model_name)
    model = BlipForConditionalGeneration.from_pretrained(model_name)
    return processor, model


def invoke_model(model_name: str, image_path: str) -> str:
    """
    Generates a caption for a single image using the specified model.

    Args:
        model_name (str): The name of the Hugging Face model to use.
        image_path (str): The local file path to the image (png or jpeg).

    Returns:
        str: The generated caption for the image.

    Raises:
        FileNotFoundError: If the image file does not exist at the provided path.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Load processor and model
    processor, model = load_model(model_name)

    # Open and convert the image to RGB
    image = Image.open(image_path).convert("RGB")

    # Preprocess the image
    inputs = processor(images=image, return_tensors="pt")

    # Generate caption
    with torch.no_grad():
        generated_ids = model.generate(**inputs)
        generated_text = processor.decode(generated_ids[0], skip_special_tokens=True)

    return generated_text


def upload_image():
    """
    Opens a file dialog to allow the user to upload an image file.
    Displays the uploaded image in the application and saves its file path.
    """
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if file_path:
        try:
            # Display the uploaded image
            img = Image.open(file_path)
            img.thumbnail((500, 500))
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk

            # Save file path for later processing
            image_label.file_path = file_path
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {str(e)}")


def handle_generate():
    """
    Handles the generation of a description for the uploaded image.
    Calls the invoke_model function and displays the result.
    """
    if hasattr(image_label, 'file_path'):
        try:
            description = invoke_model('RidzIn/Pokemon-Describer', image_label.file_path)
            description_text.set(description)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate description: {str(e)}")
    else:
        messagebox.showwarning("No Image", "Please upload an image first.")


# Create the main application window
root = tk.Tk()
root.title("Pokemon Description Generator")
root.geometry("2560x1440")

# GUI Components
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

generate_button = tk.Button(root, text="Generate Description", command=handle_generate)
generate_button.pack(pady=10)

image_label = tk.Label(root)
image_label.pack(pady=10)

description_text = tk.StringVar()
description_label = tk.Label(root, textvariable=description_text, wraplength=800, justify="center")
description_label.pack(pady=10)

# Run the application
root.mainloop()
