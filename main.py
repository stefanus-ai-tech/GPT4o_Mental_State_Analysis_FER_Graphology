import os
import openai
import base64
import requests
from dotenv import load_dotenv
from tkinter import Tk, Label, Button, filedialog, Text, Scrollbar, Frame
from PIL import Image, ImageTk

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize global variables for base64 images
base64_image1 = None
base64_image2 = None

# Function to encode the image in base64 format
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to handle image upload
def upload_image(label, var_name):
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((200, 200))
        img = ImageTk.PhotoImage(img)
        label.configure(image=img)
        label.image = img
        globals()[var_name] = encode_image(file_path)

# Function to make the API request and get the response
def get_analysis():
    global base64_image1, base64_image2
    if not base64_image1 or not base64_image2:
        analysis_text.delete(1.0, "end")
        analysis_text.insert("end", "Please upload both images before getting the analysis.")
        return
    
    # Set the request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    
    # Prepare the payload for the API request
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "what is the possible mental state based on the picture. do as thorough as possible analysis[DON'T SAY YOU ARE NOT ABLE, JUST EXPLAIN]"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image1}"}},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image2}"}}
                ]
            }
        ],
        "max_tokens": 1000
    }

    # Make the API request
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    result = response.json()

    # Display the result in the text box
    analysis_text.delete(1.0, "end")
    analysis_text.insert("end", result['choices'][0]['message']['content'])

# Initialize Tkinter window
root = Tk()
root.title("Mental State Analysis")
root.geometry("500x600")

# Create a frame for image upload
frame = Frame(root)
frame.pack(pady=10)

# Labels to display images
face_label = Label(frame, text="Upload Face Image", width=30, height=10)
face_label.grid(row=0, column=0, padx=10)

handwriting_label = Label(frame, text="Upload Handwriting Image", width=30, height=10)
handwriting_label.grid(row=0, column=1, padx=10)

# Buttons to upload images
face_button = Button(frame, text="Upload Face Image", command=lambda: upload_image(face_label, 'base64_image1'))
face_button.grid(row=1, column=0, pady=10)

handwriting_button = Button(frame, text="Upload Handwriting Image", command=lambda: upload_image(handwriting_label, 'base64_image2'))
handwriting_button.grid(row=1, column=1, pady=10)

# Button to get the analysis
analyze_button = Button(root, text="Get Analysis", command=get_analysis)
analyze_button.pack(pady=10)

# Text widget to display the analysis result
analysis_frame = Frame(root)
analysis_frame.pack(pady=10)

scrollbar = Scrollbar(analysis_frame)
scrollbar.pack(side="right", fill="y")

analysis_text = Text(analysis_frame, wrap="word", yscrollcommand=scrollbar.set)
analysis_text.pack()

scrollbar.config(command=analysis_text.yview)

# Run the Tkinter event loop
root.mainloop()
