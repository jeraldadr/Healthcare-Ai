import socket

PORT = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("172.17.0.1", PORT))
server.listen(1)
conn, addr = server.accept()

while True:
    data = conn.recv(1024)  # Receive data
    if not data:
        break
    print("Received:", data.decode())  # Process data
