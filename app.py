import yaml
import subprocess
import platform
import sys
import io
import re
from flask import Flask, render_template

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

app = Flask(__name__)

def load_config():
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config.get('devices', [])
    except Exception as e:
        print(f"Config error: {str(e)}")
        return []

def ping_device(ip):
    try:
        # Configure command based on OS
        if platform.system().lower() == 'windows':
            command = ['ping', '-n', '1', '-w', '1000', ip]
        else:
            command = ['ping', '-c', '1', '-W', '1', ip]
        
        # Configure subprocess flags
        kwargs = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'universal_newlines': False
        }
        if sys.platform == "win32":
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW

        result = subprocess.run(command, **kwargs)
        
        # Decode output with error handling
        output = result.stdout.decode('utf-8', errors='ignore')
        
        # Windows-specific checks
        if sys.platform == "win32":
            # Check for both success conditions
            status = result.returncode == 0 and "TTL=" in output
            time_match = re.search(r'zeit=(\d+)ms', output, re.IGNORECASE) or \
                         re.search(r'time=(\d+)ms', output, re.IGNORECASE)
        else:
            status = result.returncode == 0
            time_match = re.search(r'time=([\d.]+)\s*ms', output)
        
        if status and time_match:
            return True, float(time_match.group(1))
        return status, 0.0
        
    except Exception as e:
        print(f"Ping error for {ip}: {str(e)}")
        return False, 0

@app.route('/')
def index():
    devices = []
    for device in load_config():
        status, ping_time = ping_device(device['ip'])
        devices.append({
            'name': device['name'],
            'ip': device['ip'],
            'status': 'Online' if status else 'Offline',
            'ping_time': f"{ping_time:.1f} ms" if status else "Offline",
            'status_class': 'online' if status else 'offline'
        })
    return render_template('index.html', devices=devices)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
