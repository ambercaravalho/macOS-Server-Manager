import subprocess
import os
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')

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
