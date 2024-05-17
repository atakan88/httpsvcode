import subprocess

# Define the commands to execute
commands = [
    "sudo apt update",
    "sudo apt install python3-pip",
    "sudo pip install --upgrade pip",
    "sudo pip3 install geocoder",
    "sudo pip install psutil",
    "sudo pip install paho-mqtt",
    "sudo pip3 install tb-mqtt-client",
    "sudo pip install pymmh3"
]

# Execute each command
for command in commands:
    subprocess.run(command, shell=True)
