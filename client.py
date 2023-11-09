# Author : Nova Thomas

import socket

IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

def main():
    print("Starting the Client")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    while True:
        data = client.recv(SIZE).decode(FORMAT)

        if "@" in data:
            cmd, msg = data.split("@", 1)  # Split only once
            print("Would you like to UPLOAD, DELETE, or LOGOUT?")
            if cmd == "OK":
                print(f"{msg}")
            elif cmd == "DISCONNECTED":
                print(f"{msg}")
                break
        else:
            print("Received unexpected data:", data)

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "UPLOAD":
            # Code for adding file to upload
            client.send(cmd.encode(FORMAT))
        elif cmd == "DELETE":
            # Code for adding the name of the file to be deleted
            client.send(cmd.encode(FORMAT))
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()