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
                # Code for receiving a file
                break
            elif cmd == "DELETE":
                # Code for deleting a file
                break
        
        print(f"{self.client_address} disconnected")

def main():
    print("Starting the server")
    server = socketserver.TCPServer(ADDR, MyTCPHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()