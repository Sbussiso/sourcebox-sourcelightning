import openai
import requests
import os
import platform
import ctypes  # For Windows wallpaper
from io import BytesIO
from PIL import Image

# Replace with your OpenAI API key
openai.api_key = 'your_openai_api_key_here'

# Function to generate image from OpenAI
def generate_image(prompt):
    response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
    image_url = response['data'][0]['url']
    return image_url

# Function to download the image and save it locally
def save_image(image_url, file_path='generated_image.png'):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save(file_path)
    return file_path

# Function to set wallpaper for Windows
def set_wallpaper_windows(image_path):
    abs_path = os.path.abspath(image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)

# Function to set wallpaper for Linux (GNOME example)
def set_wallpaper_linux(image_path):
    abs_path = os.path.abspath(image_path)
    command = f"gsettings set org.gnome.desktop.background picture-uri 'file://{abs_path}'"
    os.system(command)

# Function to detect OS and set wallpaper accordingly
def set_wallpaper(image_path):
    current_os = platform.system()
    if current_os == 'Windows':
        set_wallpaper_windows(image_path)
    elif current_os == 'Linux':
        set_wallpaper_linux(image_path)
    else:
        print(f"OS {current_os} not supported for setting wallpaper")

def main():
    # Get the prompt from the user
    prompt = input("Enter a prompt for the image: ")

    # Generate the image from OpenAI
    print("Generating image...")
    image_url = generate_image(prompt)

    # Save the image locally
    print("Saving image...")
    image_path = save_image(image_url, 'generated_image.png')

    # Set the image as the wallpaper
    print("Setting wallpaper...")
    set_wallpaper(image_path)
    print("Wallpaper set successfully!")

if __name__ == '__main__':
    main()
