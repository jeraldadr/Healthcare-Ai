import socket

SERVER_IP = "172.17.0.1"  # Replace with your PC's IP address
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, PORT))

while True:
    data = "Hello from Pi!"  # Replace with transcribed text or raw audio
    sock.sendall(data.encode())  # Send data
