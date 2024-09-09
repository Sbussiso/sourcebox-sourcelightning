import os
import subprocess
import tempfile

def clone_repo():
    # Define the repository URL
    repo_url = "https://github.com/SourceBox-LLC/SourceLightning-FileReaderApp.git"
    
    # Get the current working directory
    cwd = os.getcwd()
    
    # Create a temporary directory in the current working directory
    with tempfile.TemporaryDirectory(dir=cwd) as temp_dir:
        print(f"Cloning repository to temporary folder in CWD: {temp_dir}")
        
        # Clone the repository using subprocess
        try:
            subprocess.run(["git", "clone", repo_url, temp_dir], check=True)
            print(f"Repository successfully cloned to {temp_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e}")

if __name__ == "__main__":
    clone_repo()
