import tempfile
import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv
import random
import shutil



load_dotenv()

client = OpenAI()



def test_config():

    def create_temp_directory():
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Define the path for the build-config.yaml file
        config_file_path = os.path.join(temp_dir, 'build-config.yaml')

        # Example configuration data
        config = {
            'project': {
                'name': 'Math assistant',
                'version': '1.0.0',
                'description': 'a search agent with access to the Math toolkit.'
            },
            'build': {
                'model': 'Anthropic',
                'toolkits': ['Math'],
                'prompt': 'You are a helpful math assistant.'
            }
        }

        # Write the configuration to the YAML file
        with open(config_file_path, 'w') as file:
            yaml.dump(config, file)

        return config_file_path

    def read_config_file(config_file_path):
        # Check if the file exists
        if not os.path.exists(config_file_path):
            print("Configuration file not found.")
            return None

        # Read the configuration from the YAML file
        with open(config_file_path, 'r') as file:
            config = yaml.safe_load(file)

        print("Configuration read from file:")
        print(config)
        return config
    
    config_file_path = create_temp_directory()
    config = read_config_file(config_file_path)
    return config





def gather_templates(config):
    # Read the configuration from the YAML file
    template_dict = {}

    # Define paths for start and end templates
    start_template_path = os.path.join('lightning-plates', 'start template', 'start.txt')
    end_template_path = os.path.join('lightning-plates', 'end template', 'end.txt')

    # Read start template
    try:
        with open(start_template_path, 'r') as file:
            start_template = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{start_template_path}' was not found.")
        return  # Exit the function if the file is not found

    template_dict["start"] = start_template

    # Map models to their respective file paths
    model_paths = {
        'Anthropic': os.path.join('lightning-plates', 'main template', 'models', 'anthropic.txt'),
        'OpenAI': os.path.join('lightning-plates', 'main template', 'models', 'openai.txt'),
        'Mistral': os.path.join('lightning-plates', 'main template', 'models', 'mistral.txt'),
        'Meta Llama': os.path.join('lightning-plates', 'main template', 'models', 'llama3.txt')
    }

    # Get model template
    model = config['build']['model']
    if model in model_paths:
        with open(model_paths[model], 'r') as file:
            model_template = file.read()
        template_dict["model template"] = model_template
    else:
        print('Error: no model found')

    # Map tools to their respective file paths
    tool_paths = {
        'Duck Duck Go Search': os.path.join('lightning-plates', 'main template', 'tools', 'duckduckgo_search.txt'),
        'Wikipedia Search': os.path.join('lightning-plates', 'main template', 'tools', 'wikipedia_search.txt'),
        'Multiply': os.path.join('lightning-plates', 'main template', 'tools', 'multiply.txt'),
        'Replit Code Interpreter': os.path.join('lightning-plates', 'main template', 'tools', 'replit-code-interpreter.txt'),
        'Local Machine': os.path.join('lightning-plates', 'main template', 'tools', 'local-machine.txt'),
        'Stack Exchange': os.path.join('lightning-plates', 'main template', 'tools', 'stackexchange.txt')
    }

    # Get tool templates
    toolkits = config['build']['toolkits']
    tool_templates_list = []

    for tool in toolkits:
        if tool in tool_paths:
            with open(tool_paths[tool], 'r') as file:
                tool_content = file.read()
            tool_templates_list.append(tool_content)
        else:
            print('Error: no tools found')

    template_dict["toolkits"] = tool_templates_list

    # Read end template
    with open(end_template_path, 'r') as file:
        end_template = file.read()

    template_dict["end"] = end_template

    return template_dict





# compile templates into one
def compile_templates(templates):
    # Initialize an empty string to hold the compiled templates
    compiled_template = ""

    # Iterate through the templates in the dictionary and concatenate them
    for key, value in templates.items():
        if isinstance(value, list):  # Check if the value is a list (like toolkits)
            for item in value:
                compiled_template += f"{item}\n\n"  # Add each item followed by two newlines for separation
        else:
            compiled_template += f"{value}\n\n"  # Add each template followed by two newlines for separation

    return compiled_template  # Return the compiled string


        
def gpt_rewrite(compiled_template):
    try:
        # Call GPT API with formatted history and vector results
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": '''
                You are a template compiler and expert programmer.
                You are to take the template pieces you are given and re format them to create one final template.

                RULES:
                - no redundency or errors.
                - write out the full entire script.
                - all imports go at the top.
                - tools go together
                '''},
                {"role": "user", "content": compiled_template}
            ]
        )

        response_content = response.choices[0].message.content
        return response_content

    except Exception as e:
        print(f"Error generating GPT response: {e}")
        return f"Error: {e}"




def generate_requirements(final_template, build_file_path):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": '''
                You are a requirements.txt writer.
                Your only function is to generate the latest requirements.txt based off of code you are given.

                RULES:
                Only generate requirements.txt based off the code input
                Must install the latest versions of each package

                in: code ==> out: requirements.txt

                Example:
                package1
                package2
                package3
                package4
                package5
                '''},
                {"role": "user", "content": final_template}
            ]
        )

        response_content = response.choices[0].message.content

        # Return the requirements content instead of writing it here
        return response_content

    except Exception as e:
        print(f"Error generating GPT response: {e}")
        return f"Error: {e}"





def export_final_template(final_template, build_file_path):
    # Generate a random 5 digit number for unique folder naming
    random_number = random.randint(10000, 99999)
    folder_name = f'agent_template_{random_number}'
    print(f"Generated random 5 digit number: {random_number}")

    # Create a directory in the current working directory
    cwd = os.getcwd()
    output_dir = os.path.join(cwd, folder_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Directory created at: {output_dir}")

    # Define the file names
    template_file_name = 'user_template.py'
    requirements_file_name = 'requirements.txt'
    build_file_name = 'build-config.yaml'

    # Define the paths for the new files
    template_file_path = os.path.join(output_dir, template_file_name)
    requirements_file_path = os.path.join(output_dir, requirements_file_name)
    build_file_destination_path = os.path.join(output_dir, build_file_name)

    # Open the file in write mode and write the final_template to it
    with open(template_file_path, 'w') as file:
        file.write(final_template)

    # Copy the build configuration file to the new directory
    with open(build_file_path, 'r') as src_file:
        with open(build_file_destination_path, 'w') as dest_file:
            dest_file.write(src_file.read())

    print(f"Template file exported to: {template_file_path}")
    print(f"Build file exported to: {build_file_destination_path}")

    return output_dir, template_file_path, requirements_file_path, build_file_destination_path


# Example usage
if __name__ == "__main__":
    
    config_file = test_config()
    templates = gather_templates(config_file)

    print("\n\nCOMPILED TEMPLATE:\n\n")
    compiled_template = compile_templates(templates)
    print(compiled_template)


    print("\n\nFINAL TEMPLATE:\n\n")
    final_template = gpt_rewrite(compiled_template)
    print(final_template)


    print("\n\nGENERATED REQUIREMENTS:\n\n")
    requirements = generate_requirements(final_template)
    print(requirements)


    print("\n\nExporting Template.........\n\n")
    export_final_template(final_template)
