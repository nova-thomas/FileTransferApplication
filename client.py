# Author : Nova Thomas

import socket
import os

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
            cmd, msg = data.split("@", 1)
            print("Would you like to UPLOAD, DELETE, or LOGOUT?")
            if cmd == "OK":
                print(f"{msg}")
            elif cmd == "DISCONNECTED":
                print(f"{msg}")
                break
        else:
            print("Received unexpected data:", data)

        user_input = input("> ")
        cmd, *params = user_input.split()

        if cmd == "UPLOAD":
            if len(params) == 1:
                filename = params[0]
                if os.path.exists(filename):
                    client.send(f"{cmd}@{filename}".encode(FORMAT))
                    with open(filename, "rb") as file:
                        while True:
                            data = file.read(SIZE)
                            if not data:
                                break
                            client.send(data)
                    response = client.recv(SIZE).decode(FORMAT)
                    print(response)
                else:
                    print(f"File {filename} does not exist.")
            else:
                print("Usage: UPLOAD <filename>")
        elif cmd == "DELETE":
            if len(params) == 1:
                filename = params[0]
                client.send(f"{cmd}@{filename}".encode(FORMAT))
                response = client.recv(SIZE).decode(FORMAT)
                print(response)
            else:
                print("Usage: DELETE <filename>")
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
        else:
            print("Invalid command. Please use UPLOAD, DELETE, or LOGOUT.")

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()