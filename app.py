import os
import subprocess
import tempfile
import shutil
from flask import Flask, render_template, send_from_directory, abort, request
from flask import Flask, request, jsonify, render_template, send_file, session
from flask_cors import CORS
import yaml
import os
import random
import shutil
from build import gather_templates, compile_templates, gpt_rewrite, export_final_template, generate_requirements
import logging
import zipfile
from datetime import timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)  # Set session timeout to one hour
CORS(app)  # Enable CORS if needed

# App repository URLs
FILE_READER_REPO = "https://github.com/SourceBox-LLC/SourceLightning-FileReaderApp.git"
PC_SCANNER_REPO = "https://github.com/SourceBox-LLC/SourceLighting-PC-scannerApp.git"
WALLPAPER_GEN_REPO = "https://github.com/SourceBox-LLC/SourceLightning-WallpaperGenerator.git"
VANILLA_GPT_REPO = "https://github.com/SourceBox-LLC/SourceLightning-Vanilla-GPT.git"
VANILLA_MISTRAL_REPO = "https://github.com/SourceBox-LLC/SourceLightning-Vanilla-Mistral.git"
VANILLA_GEMINI_REPO = "https://github.com/SourceBox-LLC/SourceLightning-Vanilla-Gemini.git"
VANILLA_CLAUD_REPO = "https://github.com/SourceBox-LLC/SourceLightning-Vanilla-Claude.git"

# Agent repository URLs
GOOGLE_AGENT_REPO = "https://github.com/SourceBox-LLC/SourceLightning-GoogleAgent.git"
CODE_AGENT_REPO = "https://github.com/SourceBox-LLC/SourceLightning-CodeAgent.git"
LOCAL_COMMAND_AGENT_REPO = "https://github.com/SourceBox-LLC/SourceLightning-LocalCommandAgent.git"
FINANCE_AGENT_REPO = "https://github.com/SourceBox-LLC/SourceLightning-FinanceAgent.git"

# Function to clone the repo and zip it inside a parent folder
def clone_and_zip_repo(REPO_URL, repo_name):
    # Get the current working directory
    cwd = os.getcwd()
    
    # Create a temporary directory in the current working directory
    temp_dir = tempfile.mkdtemp(dir=cwd)
    print(f"Cloning repository to temporary folder in CWD: {temp_dir}")
    
    try:
        # Clone the repository using subprocess
        subprocess.run(["git", "clone", REPO_URL, temp_dir], check=True)
        print(f"Repository successfully cloned to {temp_dir}")
        
        # Create a parent folder in the temp directory named after the repo
        parent_folder_name = f"{repo_name}_repo"
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
def serve_repo(REPO_URL, repo_name):
    # Clone and zip the repo, then get the zip file path
    zip_file_path = clone_and_zip_repo(REPO_URL, repo_name)
        
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

@app.route('/build-landing')
def build_landing():
    return render_template('build_landing.html')

# File reader download route
@app.route('/download/file_reader')
def download_file_reader():
    return serve_repo(FILE_READER_REPO, "file_reader")

# PC scanner download route
@app.route('/download/pc_scanner')
def download_pc_scanner():
    return serve_repo(PC_SCANNER_REPO, "pc_scanner")

# wallpaper generator route
@app.route('/download/wallpaper_gen')
def wallpaper_gen():
    return serve_repo(WALLPAPER_GEN_REPO, "wallpaper_gen")

# vanilla gpt route
@app.route('/download/vanilla_gpt')
def vanilla_gpt():
    return serve_repo(VANILLA_GPT_REPO, "vanilla_gpt")

# mistral route
@app.route('/download/vanilla_mistral')
def vanilla_mistral():
    return serve_repo(VANILLA_MISTRAL_REPO, "vanilla_mistral")

# gemini route
@app.route('/download/vanilla_gemini')
def vanilla_gemini():
    return serve_repo(VANILLA_GEMINI_REPO, "vanilla_gemini")

#claud route
@app.route('/download/vanilla_claud')
def vanilla_claud():
    return serve_repo(VANILLA_CLAUD_REPO, "vanilla_claud")






# google agent route
@app.route('/download/google_agent')
def google_agent():
    return serve_repo(GOOGLE_AGENT_REPO, "google_agent")

# code agent route
@app.route('/download/code_agent')
def code_agent():
    return serve_repo(CODE_AGENT_REPO, "code_agent")

# local command agent route
@app.route('/download/local_command_agent')
def local_command_agent():
    return serve_repo(LOCAL_COMMAND_AGENT_REPO, "local_command_agent")

# finance agent route
@app.route('/download/finance_agent')
def finance_agent():
    return serve_repo(FINANCE_AGENT_REPO, "finance_agent")


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






#LIGHTNING BUILDER

@app.route('/build')
def build():
    return render_template('build.html')

@app.route('/generate-config', methods=['POST'])
def generate_config():
    data = request.json
    logger.info(f"Received data for configuration generation: {data}")

    config_data = {
        'project': {
            'name': data.get('agent_name'),
            'version': '1.0.0',
            'description': data.get('agent_description')
        },
        'build': {
            'model': data.get('selected_model'),
            'toolkits': data.get('selected_toolkits', []),
            'prompt': data.get('agent_prompt')
        }
    }

    cwd = os.getcwd()
    config_file_path = os.path.join(cwd, 'build-config.yaml')

    try:
        with open(config_file_path, 'w') as file:
            yaml.dump(config_data, file)
        logger.info(f"Configuration file created at: {config_file_path}")
        session['config_file_path'] = config_file_path  # Store in session
    except Exception as e:
        logger.error(f"Error writing configuration file: {e}")
        return jsonify({'error': 'Failed to write configuration file.'}), 500

    return jsonify({
        'message': 'Configuration file generated successfully',
        'config_file_path': config_file_path
    })



@app.route('/custom-config', methods=['POST'])
def custom_config():
    data = request.json
    logger.info("Received request for custom configuration.")
    
    config_content = data.get('config')
    logger.debug(f"Config content received: {config_content}")

    if not config_content:
        logger.error("No configuration content provided.")
        return jsonify({'error': 'No configuration content provided.'}), 400

    try:
        # Parse the YAML configuration content
        config_data = yaml.safe_load(config_content)
        logger.info(f"Parsed configuration data: {config_data}")

        # Write the configuration to a file
        cwd = os.getcwd()
        config_file_path = os.path.join(cwd, 'build-config.yaml')
        with open(config_file_path, 'w') as file:
            yaml.dump(config_data, file)
        logger.info(f"Custom configuration file created at: {config_file_path}")

        # Store the configuration data in the session
        session['config_data'] = config_data
        session['config_file_path'] = config_file_path
        logger.info("Configuration data stored in session.")

        return jsonify({
            'message': 'Custom configuration processed successfully',
            'config_file_path': config_file_path,
            'config_data': config_data
        })
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        return jsonify({'error': 'Failed to parse configuration file.'}), 500
    except Exception as e:
        logger.error(f"Error writing custom configuration file: {e}")
        return jsonify({'error': 'Failed to write custom configuration file.'}), 500



@app.route('/display-config')
def display_config():
    logger.info("Received request to display configuration.")
    
    config_file_path = session.get('config_file_path')
    logger.debug(f"Config file path from session: {config_file_path}")

    if config_file_path is None or not os.path.exists(config_file_path):
        logger.error("Configuration file not found.")
        return jsonify({'error': 'Configuration file not found.'}), 400

    logger.info(f"Reading configuration from: {config_file_path}")

    try:
        with open(config_file_path, 'r') as file:
            config_data = yaml.safe_load(file)
            logger.info("Configuration data successfully loaded.")
    except Exception as e:
        logger.error(f"Error reading configuration file: {e}")
        return jsonify({'error': 'Failed to read configuration file.'}), 500

    logger.info("Returning configuration data as JSON.")
    return jsonify(config_data)

@app.route('/assemble-config', methods=['POST'])
def assemble_config():
    config_file_path = session.get('config_file_path')  # Get from session

    if config_file_path is None or not os.path.exists(config_file_path):
        logger.error("Configuration file not found.")
        return jsonify({'error': 'Configuration file not found.'}), 400

    logger.info(f"Reading configuration from: {config_file_path}")

    try:
        with open(config_file_path, 'r') as file:
            config_data = yaml.safe_load(file)
            logger.info("Configuration data successfully loaded.")
    except Exception as e:
        logger.error(f"Error reading configuration file: {e}")
        return jsonify({'error': 'Failed to read configuration file.'}), 500

    try:
        logger.info("Gathering templates based on the configuration.")
        templates = gather_templates(config_data)

        logger.info("Compiling templates into a single string.")
        compiled_template = compile_templates(templates)

        logger.info("Rewriting the compiled template using GPT.")
        final_template = gpt_rewrite(compiled_template)

        logger.info("Generating requirements based on the final template.")
        requirements = generate_requirements(final_template, config_file_path)

        logger.info("Exporting the final template and requirements to the current working directory.")
        output_dir, template_file_path, requirements_file_path, build_file_destination_path = export_final_template(final_template, config_file_path)

        # Write the requirements to the file
        with open(requirements_file_path, 'w') as req_file:
            req_file.write(requirements)

        # Store the paths in the session
        session['template_file_path'] = template_file_path
        session['requirements_file_path'] = requirements_file_path
        session['build_file_destination_path'] = build_file_destination_path

        logger.info(f"Template file path: {template_file_path}")
        logger.info(f"Requirements file path: {requirements_file_path}")
        logger.info(f"Build file path: {build_file_destination_path}")

        logger.info("Template assembled successfully.")
    except Exception as e:
        logger.error(f"Error during template assembly: {e}")
        return jsonify({'error': 'Failed to assemble template.'}), 500

    return jsonify({
        'message': 'Template assembled successfully',
        'file_path': template_file_path,
        'requirements_path': requirements_file_path,
        'build_file_path': build_file_destination_path,
        'final_template': final_template,
        'requirements': requirements
    })

@app.route('/download-agent', methods=['POST'])
def download_agent():
    # Retrieve paths from the session
    template_file_path = session.get('template_file_path')
    requirements_file_path = session.get('requirements_file_path')
    build_file_destination_path = session.get('build_file_destination_path')

    logger.debug(f"Attempting to download files with paths: {template_file_path}, {requirements_file_path}, {build_file_destination_path}")

    # Check if any file path is missing from the session
    if not all([template_file_path, requirements_file_path, build_file_destination_path]):
        logger.error("One or more file paths are missing from the session.")
        return jsonify({'error': 'File paths are missing.'}), 400

    # Check if each file exists and log if any are missing
    missing_files = []
    for path, name in zip(
        [template_file_path, requirements_file_path, build_file_destination_path],
        ['Template file', 'Requirements file', 'Build file']
    ):
        if not os.path.exists(path):
            missing_files.append(name)
            logger.error(f"{name} not found at path: {path}")

    if missing_files:
        return jsonify({'error': f"Files not found: {', '.join(missing_files)}"}), 400

    # Create the archive directory if it doesn't exist
    archive_dir = os.path.join(os.getcwd(), 'archive')
    os.makedirs(archive_dir, exist_ok=True)

    zip_file_name = f"agent_template_{random.randint(10000, 99999)}.zip"
    zip_file_path = os.path.join(archive_dir, zip_file_name)
    logger.info(f"Creating zip file: {zip_file_path}")

    try:
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file_path in [template_file_path, requirements_file_path, build_file_destination_path]:
                logger.debug(f"Adding file to zip: {file_path}")
                zipf.write(file_path, arcname=os.path.basename(file_path))
        
        logger.info(f"Successfully created zip file: {zip_file_path}")

        # Send the zip file to the user
        return send_file(zip_file_path, as_attachment=True, download_name=zip_file_name)

    except Exception as e:
        logger.error(f"Error while creating or sending the zip file: {e}")
        return jsonify({'error': 'Failed to create or send the zip file.'}), 500




@app.route('/delete-files', methods=['POST'])
def delete_files():
    # Retrieve paths from the session
    template_file_path = session.get('template_file_path')
    requirements_file_path = session.get('requirements_file_path')
    build_file_destination_path = session.get('build_file_destination_path')
    zip_file_path = session.get('zip_file_path')

    # Determine the directory to delete
    if template_file_path:
        agent_dir = os.path.dirname(template_file_path)
    else:
        logger.error("Template file path is missing.")
        return jsonify({'error': 'Template file path is missing.'}), 400

    # Delete the zip file
    if zip_file_path and os.path.exists(zip_file_path):
        try:
            os.remove(zip_file_path)
            logger.info(f"Deleted zip file: {zip_file_path}")
        except Exception as e:
            logger.error(f"Error deleting zip file {zip_file_path}: {e}")
            return jsonify({'error': 'Failed to delete zip file.'}), 500

    # Delete the agent template directory
    if os.path.exists(agent_dir):
        try:
            shutil.rmtree(agent_dir)
            logger.info(f"Deleted agent directory: {agent_dir}")
        except Exception as e:
            logger.error(f"Error deleting agent directory {agent_dir}: {e}")
            return jsonify({'error': 'Failed to delete agent directory.'}), 500

    return jsonify({'message': 'Files and directory deleted successfully.'})




@app.route('/upload-config', methods=['POST'])
def upload_config():
    data = request.json
    config_content = data.get('config')

    if not config_content:
        return jsonify({'error': 'No configuration content provided.'}), 400

    config_file_path = os.path.join(os.getcwd(), 'build-config.yaml')

    try:
        with open(config_file_path, 'w') as file:
            file.write(config_content)
        logger.info(f"Custom configuration file uploaded at: {config_file_path}")
        session['config_file_path'] = config_file_path  # Store in session
    except Exception as e:
        logger.error(f"Error writing custom configuration file: {e}")
        return jsonify({'error': 'Failed to write custom configuration file.'}), 500

    return jsonify({'message': 'Custom configuration uploaded successfully'})








if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # Use the PORT environment variable if available, default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
