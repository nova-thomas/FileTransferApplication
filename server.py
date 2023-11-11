# Author : Nova Thomas

# Server code
import socketserver
import os

IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
FORMAT = "utf-8"
SERVER_PATH = "server"

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        if not os.path.exists(SERVER_PATH):
            os.makedirs(SERVER_PATH)
        print(f"NEW CONNECTION: {self.client_address} connected.")
        self.request.sendall("OK@Welcome to the server".encode(FORMAT))

        try:
            while True:
                data = self.request.recv(1024).decode(FORMAT)
                if not data:
                    break

                data = data.split("@")
                cmd = data[0]
                send_data = "OK@"

                print(f"Received command: {cmd}")

                if cmd == "LOGOUT":
                    break
                elif cmd == "UPLOAD":
                    if len(data) == 2:
                        filename = data[1]
                        file_path = os.path.join(SERVER_PATH, filename)

                        with open(file_path, "wb") as file:
                            try:
                                while True:
                                    data = self.request.recv(1024)
                                    if not data:
                                        break
                                    file.write(data)

                                # Send a special message to signal the end of file transmission
                                self.request.sendall("UPLOAD_COMPLETE".encode(FORMAT))

                                # Receive the "UPLOAD_COMPLETE" message from the client
                                upload_complete_message = self.request.recv(1024).decode(FORMAT)
                                if upload_complete_message == "UPLOAD_COMPLETE":
                                    print(f"File {filename} uploaded successfully")
                                else:
                                    print("Error: File upload incomplete or failed")

                                # Receive the next command from the client
                                data = self.request.recv(1024).decode(FORMAT)
                                if not data:
                                    break
                                print(f"Received {filename}")
                                send_data += "File uploaded successfully"
                            finally:
                                file.close()
                                
                    else:
                        send_data += "Invalid UPLOAD command format"
                elif cmd == "DELETE":
                    if len(data) == 2:
                        filename = data[1]
                        file_path = os.path.join(SERVER_PATH, filename)

                        if os.path.exists(file_path):
                            os.remove(file_path)
                            send_data += f"File {filename} deleted successfully"
                        else:
                            send_data += f"File {filename} does not exist"
                            print("File does not exist")
                    else:
                        send_data += "Invalid DELETE command format"
                self.request.sendall(send_data.encode(FORMAT))

        except Exception as e:
            print(f"Error: {e}")
        finally:
            print(f"{self.client_address} disconnected")
            self.request.close()

def main():
    print("Starting the server")
    server = socketserver.TCPServer(ADDR, MyTCPHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()