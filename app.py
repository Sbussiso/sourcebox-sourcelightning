import os
import subprocess
import tempfile
import shutil
from flask import Flask, render_template, send_from_directory, abort, request

app = Flask(__name__)

# App repository URLs
FILE_READER_REPO = "https://github.com/SourceBox-LLC/SourceLightning-FileReaderApp.git"
PC_SCANNER_REPO = "https://github.com/SourceBox-LLC/SourceLighting-PC-scannerApp.git"
WALLPAPER_GEN_REPO = "https://github.com/SourceBox-LLC/SourceLightning-WallpaperGenerator.git"
VANILLA_GPT_REPO = "https://github.com/SourceBox-LLC/SourceLightning-Vanilla-GPT.git"
VANILLA_MISTRAL_REPO = "https://github.com/SourceBox-LLC/SourceLightning-Vanilla-Mistral.git"
VANILLA_GEMINI_REPO = "https://github.com/SourceBox-LLC/SourceLightning-Vanilla-Gemini.git"
VANILLA_CLAUD_REPO = "https://github.com/SourceBox-LLC/SourceLightning-Vanilla-Claude.git"

# Function to clone the repo and zip it inside a parent folder
def clone_and_zip_repo(REPO_URL):
    # Get the current working directory
    cwd = os.getcwd()
    
    # Create a temporary directory in the current working directory
    temp_dir = tempfile.mkdtemp(dir=cwd)
    print(f"Cloning repository to temporary folder in CWD: {temp_dir}")
    
    try:
        # Clone the repository using subprocess
        subprocess.run(["git", "clone", REPO_URL, temp_dir], check=True)
        print(f"Repository successfully cloned to {temp_dir}")
        
        # Create a parent folder in the temp directory
        parent_folder_name = "file_reader_repo"
        parent_folder_path = os.path.join(temp_dir, parent_folder_name)
        os.makedirs(parent_folder_path)
        
        # Move the cloned repo contents into the parent folder
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            if item != parent_folder_name:  # Skip the parent folder itself
                shutil.move(item_path, parent_folder_path)
        
        # Create a zip file from the parent folder
        zip_filename = os.path.join(cwd, f'{parent_folder_name}.zip')
        shutil.make_archive(zip_filename.replace('.zip', ''), 'zip', temp_dir, parent_folder_name)
        print(f"Repository successfully zipped at {zip_filename}")
        
        return zip_filename
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return None
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)
        print(f"Temporary directory {temp_dir} has been removed.")

# Serve repo to user
def serve_repo(REPO_URL):
    # Clone and zip the repo, then get the zip file path
    zip_file_path = clone_and_zip_repo(REPO_URL)
        
    if zip_file_path and os.path.exists(zip_file_path):
        # Store the zip file path in the request context for deletion later
        request.zip_file_path = zip_file_path
            
        # Serve the zip file to the user for download
        return send_from_directory(os.path.dirname(zip_file_path), os.path.basename(zip_file_path), as_attachment=True)
    else:
        abort(500, description="Error cloning or zipping the repository")


@app.route('/')
def index():
    return render_template('index.html')

# File reader download route
@app.route('/download/file_reader')
def download_file_reader():
    return serve_repo(FILE_READER_REPO)

# PC scanner download route
@app.route('/download/pc_scanner')
def download_pc_scanner():
    return serve_repo(PC_SCANNER_REPO)

# wallpaper generator route
@app.route('/download/wallpaper_gen')
def wallpaper_gen():
    return serve_repo(WALLPAPER_GEN_REPO)

# vanilla gpt route
@app.route('/download/vanilla_gpt')
def vanilla_gpt():
    return serve_repo(VANILLA_GPT_REPO)

# mistral route
@app.route('/download/vanilla_mistral')
def vanilla_mistral():
    return serve_repo(VANILLA_MISTRAL_REPO)

# gemini route
@app.route('/download/vanilla_gemini')
def vanilla_gemini():
    return serve_repo(VANILLA_GEMINI_REPO)

#claud route
@app.route('/download/vanilla_claud')
def vanilla_claud():
    return serve_repo(VANILLA_CLAUD_REPO)


# After request handler to delete the zip file once it has been sent to the user
@app.after_request
def delete_zip_file(response):
    zip_file_path = getattr(request, 'zip_file_path', None)
    if zip_file_path and os.path.exists(zip_file_path):
        try:
            os.remove(zip_file_path)
            print(f"Zip file {zip_file_path} has been deleted.")
        except Exception as e:
            print(f"Error deleting zip file: {e}")
    return response



if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # Use the PORT environment variable if available, default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
