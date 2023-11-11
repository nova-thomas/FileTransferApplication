# Author : Nova Thomas

# Client code
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

    try:
        while True:
            print("Would you like to UPLOAD, DELETE, or LOGOUT?")
            user_input = input("> ")
            cmd, *params = user_input.split()

            print(f"User command: {user_input}")

            if cmd == "UPLOAD":
                if len(params) == 1:
                    filename = params[0]
                    if os.path.exists(filename):
                        file_size = os.path.getsize(filename)
                        client.send(f"{cmd}@{filename}".encode(FORMAT))
                        response = client.recv(SIZE).decode(FORMAT)
                        print(f"Server response: {response}")

                        with open(filename, "rb") as file:
                            total_sent = 0
                            while True:
                                data = file.read(SIZE)
                                if not data:
                                    break
                                client.send(data)
                                total_sent += len(data)

                                # Print upload progress as a percentage
                                progress = (total_sent / file_size) * 100
                                print(f"Uploading {filename}: {progress:.2f}%")

                        # Send a special message to signal the end of file transmission
                        client.sendall("UPLOAD_COMPLETE".encode(FORMAT))

                        # Receive the server response
                        response = client.recv(SIZE).decode(FORMAT)
                        print(f"Server response: {response}")
                    else:
                        print(f"File {filename} does not exist.")
                else:
                    print("Usage: UPLOAD <filename>")
            elif cmd == "DELETE":
                if len(params) == 1:
                    filename = params[0]
                    confirmation = input(f"Are you sure you want to delete {filename}? (yes/no): ").lower()
                    if confirmation == "yes":
                        client.send(f"{cmd}@{filename}".encode(FORMAT))
                        response = client.recv(SIZE).decode(FORMAT)
                        print(f"Server response: {response}")
                    else:
                        print("Deletion canceled.")
                else:
                    print("Usage: DELETE <filename>")
            elif cmd == "LOGOUT":
                client.send(cmd.encode(FORMAT))
                break
            else:
                print("Invalid command. Please use UPLOAD, DELETE, or LOGOUT.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Disconnected from the server.")
        client.close()

if __name__ == "__main__":
    main()