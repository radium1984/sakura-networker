# 🌸 Sakura Network Monitor 🌸

## Setup
```git clone https://github.com/radium1984/sakura-networker.git```

```cd sakura-networker```

```pip install flask pyyaml```


## Config
Edit the confing.yaml file to change the devices you want to monitor.
```
devices:
  - name: "Router"
    ip: "192.168.1.1"
  - name: "adGuard Server"
    ip: "192.168.1.2"
  - name: "Server"
    ip: "192.168.1.69"
```

## Usage
Just start the app.py with python. You can now use your browser and visit the shown IP.

```python3 app.py```
