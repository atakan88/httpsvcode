import paho.mqtt.client as paho
from tb_device_mqtt import TBDeviceMqttClient
import time
from time import sleep
import psutil
import geocoder
import json
import os
import subprocess

def bytes_to_readable(bytes, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(bytes) < 1024.0:
            return f"{bytes:.{decimal_places}f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.{decimal_places}f} PB"

konum = geocoder.ip('me')
konum = geocoder.ip('me')
latitude = konum.lat
longitude =konum.lng

running_executables = []


# MQTT broker configuration
broker = "192.168.56.101"
port = 1883
username = "aocslq25r4rp2j2gwons"
topic_pub = 'v1/devices/me/telemetry'


def on_server_side_rpc_request(request_id, request_body):
    print(request_id, request_body)
    
    # Check the method requested in the RPC
    if request_body["method"] == "TriggerShutdown1":
        # Execute the command to shut down Ubuntu VM
        try:
            # Use subprocess to execute the shutdown command
            subprocess.run(["sudo", "shutdown", "-h", "now"])
            
        except Exception as e:
            # If there's an error, respond with an error message
            print ("error: str{e}")
   
    else:
        pass  
        
        

# Create a TBDeviceMqttClient instance with the appropriate connection details
client = TBDeviceMqttClient("192.168.56.101", username="q8jx1eat6x0kxowp3dcq")

# Başlangıç zamanları
start_time_1 = time.time()
start_time_2 = time.time()

# İntervaller (saniye cinsinden)
interval_1 = 5   # Her 5 saniyede bir çalışacak kod bloğu
interval_2 = 30  # Her 30 saniyede bir çalışacak kod bloğu

    # Initialize MQTT client
pahoclient = paho.Client()
pahoclient.username_pw_set(username)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Connection to MQTT broker failed with result code {rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection from MQTT broker. Reconnecting... (RC: {rc})")
        while True:
            try:
                pahoclient.reconnect()
                break
            except Exception as e:
                print(f"Reconnection failed. Retrying... Error: {e}")
                time.sleep(5)  # Wait before retrying

# Set callback functions
pahoclient.on_connect = on_connect
pahoclient.on_disconnect = on_disconnect

# Connect to MQTT broker
try:
    pahoclient.connect(broker, port, 60)
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
    exit(1)

# Start the MQTT client loop
pahoclient.loop_start()

# Sonsuz döngü
try: 
    while True:
    
        current_time = time.time()  # Şu anki zamanı al

    # Her 5 saniyede bir çalışacak kod bloğu
        if (current_time - start_time_1) >= interval_1:
            print("Executing code block every 5 seconds...")
        
            start_time = time.time()
            disk_io_counter = psutil.disk_io_counters()
            start_read_bytes = disk_io_counter[2]
            start_write_bytes = disk_io_counter[3]

        # Wait before next measure
            time.sleep(1)
            disk_io_counter = psutil.disk_io_counters()

        # Get end Read bytes and end read time & Write bytes and end write time
            end_read_bytes = disk_io_counter[2]
            end_write_bytes = disk_io_counter[3]
            end_time = time.time()
            time_diff = end_time - start_time
    
        # Compute Read speed & Write speed :  Read Byte / second
            read_speed = (end_read_bytes - start_read_bytes)/time_diff
            write_speed = (end_write_bytes - start_write_bytes)/time_diff

        # Get CPU information
            cpu_usage = psutil.cpu_percent()

        # Get memory usage
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent

        # Get disk usage statistics
            partitions = psutil.disk_partitions()
            for partition in partitions:
                usage = psutil.disk_usage(partition.mountpoint)

            # Prepare MQTT messages
            #msg1 = json.dumps({"CPU_name2": cpu_brand})
                msg2 = json.dumps({"CPU1": cpu_usage})
                msg3 = json.dumps({"Memory1": memory_usage})
                msg4 = json.dumps({"Disk1": usage.percent})
                msg5 = json.dumps({"DiskTotal1": bytes_to_readable(usage.total)})
                msg6 = json.dumps({"DiskWriting1": bytes_to_readable(write_speed)})
                msg7 = json.dumps({"DiskReading1": bytes_to_readable(read_speed)})

            # Get IP location
            
                msg8 = '{"locationX1":"' + str(konum.lat) + '"}'
                msg9 = '{"locationY1":"' + str(konum.lng) + '"}'
        

            # Publish messages to MQTT broker
                pahoclient.publish(topic_pub, msg2)           
                pahoclient.publish(topic_pub, msg3)           
                pahoclient.publish(topic_pub, msg4)          
                pahoclient.publish(topic_pub, msg5)            
                pahoclient.publish(topic_pub, msg6)
                pahoclient.publish(topic_pub, msg7)
                pahoclient.publish(topic_pub, msg8)
                pahoclient.publish(topic_pub, msg9)
            
            start_time_1 = current_time  # Başlangıç zamanını güncelle
        

    # Her 30 saniyede bir çalışacak kod bloğu
        if (current_time - start_time_2) >= interval_2:
        
            running_executables.clear()
            processes = psutil.process_iter()
            for process in processes:
            
        # Check if the process has an associated executable path
                    exe_path = process.exe()
                    if exe_path:
                        running_executables.append({'name': process.name(), 'executable': exe_path})

            total_count = len(running_executables)
            exes = running_executables
            print("Executing code block every 30 seconds...")
            for i in range(total_count):
            
                exe = exes[i]
                message = f"Running Executable {i + 1}: {exe['name']} ({exe['executable']})"
                msgo = json.dumps({"Running Exe 1": message})
                pahoclient.publish(topic_pub, msgo)
                print(message)
                time.sleep(0.2)

            start_time_2 = current_time  # Başlangıç zamanını güncelle

            # Set the RPC request handler to the defined function
            client.set_server_side_rpc_request_handler(on_server_side_rpc_request)

            # Connect to the MQTT broker
            client.connect()

        time.sleep(1)  # CPU kullanımını düşük tutmak için kısa bir bekleme süresi ekle
except KeyboardInterrupt:
    print("Exiting...")

finally:
        # Clean up
    pahoclient.loop_stop()
    pahoclient.disconnect()
