# Author : Nova Thomas

import socketserver
import os

IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
FORMAT = "utf-8"
SERVER_PATH = "server"

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"NEW CONNECTION: {self.client_address} connected.")
        self.request.sendall("OK@Welcome to the server".encode(FORMAT))
        
        while True:
            data = self.request.recv(1024).decode(FORMAT)
            data = data.split("@")
            cmd = data[0]
            send_data = "OK@"
            
            if cmd == "LOGOUT":
                break
            elif cmd == "UPLOAD":
                filename = data[1]
                file_path = os.path.join(SERVER_PATH, filename)

                with open(file_path, "wb") as file:
                    while True:
                        data = self.request.recv(1024)
                        if not data:
                            break
                        file.write(data)

                send_data += "File uploaded successfully"
                self.request.sendall(send_data.encode(FORMAT))
            elif cmd == "DELETE":
                filename = data[1]
                file_path = os.path.join(SERVER_PATH, filename)

                if os.path.exists(file_path):
                    os.remove(file_path)
                    send_data += f"File {filename} deleted successfully"
                else:
                    send_data += f"File {filename} does not exist"

                self.request.sendall(send_data.encode(FORMAT))
        
        print(f"{self.client_address} disconnected")

def main():
    print("Starting the server")
    server = socketserver.TCPServer(ADDR, MyTCPHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()