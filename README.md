# GPT4o_Mental_State_Analysis_FER_Graphology

# GPT4o_Mental_State_Analysis_FER_Graphology

Welcome to the **GPT4o Mental State Analysis FER Graphology** project! This tutorial will guide you through setting up and running a simple Python application that analyzes mental state using face and handwriting images via the OpenAI API.

## Prerequisites

Before we start, ensure you have the following installed on your system:

1. Python (3.7+)
2. pip (Python package installer)
3. Git

## Project Setup

### Step 1: Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
git clone https://github.com/yourusername/GPT4o_Mental_State_Analysis_FER_Graphology.git
cd GPT4o_Mental_State_Analysis_FER_Graphology
```

### Step 2: Create and Activate a Virtual Environment

It's good practice to use a virtual environment for Python projects to manage dependencies. Run the following commands to create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

Install the necessary Python packages by running:

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory of the project and add your OpenAI API key:

```plaintext
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 5: Run the Application

Finally, run the application using:

```bash
python app.py
```

## Code Explanation

Here’s a breakdown of what the code does:

### Importing Modules

We start by importing necessary libraries:

```python
import os
import openai
import base64
import requests
from dotenv import load_dotenv
from tkinter import Tk, Label, Button, filedialog, Text, Scrollbar, Frame
from PIL import Image, ImageTk
```

### Loading Environment Variables

Load the OpenAI API key from a `.env` file:

```python
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
```

### Encoding Images in Base64

We define a function to encode images in base64 format:

```python
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
```

### Handling Image Upload

Functions to handle image uploads and display them:

```python
def upload_image(label, var_name):
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((200, 200))
        img = ImageTk.PhotoImage(img)
        label.configure(image=img)
        label.image = img
        globals()[var_name] = encode_image(file_path)
```

### Making the API Request

Function to make an API request to OpenAI and display the analysis:

```python
def get_analysis():
    global base64_image1, base64_image2
    if not base64_image1 or not base64_image2:
        analysis_text.delete(1.0, "end")
        analysis_text.insert("end", "Please upload both images before getting the analysis.")
        return
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    
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

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    result = response.json()

    analysis_text.delete(1.0, "end")
    analysis_text.insert("end", result['choices'][0]['message']['content'])
```

### Building the Tkinter GUI

Setting up the Tkinter GUI:

```python
root = Tk()
root.title("Mental State Analysis")
root.geometry("500x600")

frame = Frame(root)
frame.pack(pady=10)

face_label = Label(frame, text="Upload Face Image", width=30, height=10)
face_label.grid(row=0, column=0, padx=10)

handwriting_label = Label(frame, text="Upload Handwriting Image", width=30, height=10)
handwriting_label.grid(row=0, column=1, padx=10)

face_button = Button(frame, text="Upload Face Image", command=lambda: upload_image(face_label, 'base64_image1'))
face_button.grid(row=1, column=0, pady=10)

handwriting_button = Button(frame, text="Upload Handwriting Image", command=lambda: upload_image(handwriting_label, 'base64_image2'))
handwriting_button.grid(row=1, column=1, pady=10)

analyze_button = Button(root, text="Get Analysis", command=get_analysis)
analyze_button.pack(pady=10)

analysis_frame = Frame(root)
analysis_frame.pack(pady=10)

scrollbar = Scrollbar(analysis_frame)
scrollbar.pack(side="right", fill="y")

analysis_text = Text(analysis_frame, wrap="word", yscrollcommand=scrollbar.set)
analysis_text.pack()

scrollbar.config(command=analysis_text.yview)

root.mainloop()
```

This creates a simple GUI application where users can upload face and handwriting images, and get an analysis of the mental state.

## Conclusion

You now have a functioning application that uses OpenAI's API to analyze mental states from images. If you encounter any issues or have suggestions for improvement, feel free to open an issue or submit a pull request on the GitHub repository.

Happy coding!
