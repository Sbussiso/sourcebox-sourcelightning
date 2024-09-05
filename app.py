import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# Route for serving the file_reader.py file
@app.route('/download/file_reader')
def download_file_reader():
    # Set the directory where the file is located
    directory = 'static/sapps'
    filename = 'file_reader.py'
    
    # Send the file to the user
    return send_from_directory(directory, filename, as_attachment=True)


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # Use the PORT environment variable if available, default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
