import subprocess
import os
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS # Import CORS

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app) # Enable CORS for all routes

# Basic API endpoint example
@app.route('/api/status')
def get_status():
    try:
        # Example: Get uptime
        result = subprocess.run(['uptime'], capture_output=True, text=True, check=True)
        return jsonify({"status": "success", "uptime": result.stdout.strip()})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    except FileNotFoundError:
         return jsonify({"status": "error", "message": "Command 'uptime' not found."}), 500

# Endpoint to execute a shell command
@app.route('/api/command', methods=['POST'])
def execute_command():
    # --- SECURITY WARNING ---
    # Executing arbitrary commands received from an API is extremely dangerous
    # and should NOT be done in production without rigorous validation,
    # sanitization, and potentially restricting allowed commands.
    # This is for demonstration/development purposes ONLY.
    # --- END SECURITY WARNING ---

    data = request.get_json()
    if not data or 'command' not in data:
        return jsonify({"status": "error", "message": "Missing 'command' in request body"}), 400

    command_str = data['command']

    if not isinstance(command_str, str) or not command_str:
         return jsonify({"status": "error", "message": "'command' must be a non-empty string"}), 400

    try:
        # Using shell=True is also a security risk if the command string is crafted maliciously.
        # Consider splitting the command into a list if possible for better security.
        # For simplicity here, we use shell=True.
        result = subprocess.run(command_str, shell=True, capture_output=True, text=True, check=False) # Using check=False to capture output even on errors

        return jsonify({
            "status": "success",
            "command": command_str,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        })
    except Exception as e:
        # Catching broad Exception for unexpected issues during subprocess run
        return jsonify({"status": "error", "command": command_str, "message": str(e)}), 500

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # Serve index.html for any path that doesn't match a static file
        # This allows React Router to handle client-side routing
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Make sure to use 0.0.0.0 to be accessible on the network
    app.run(host='0.0.0.0', port=5000, debug=True) # Use debug=False in production
