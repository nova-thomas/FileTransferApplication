# Author : Nova Thomas

from cgitb import handler
import os
import socket
import threading

IP = "localhost" ### gethostname()
PORT = 4450
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"

def handle_client (conn,addr):
    print(f"NEW CONNECTION: {addr} connected.")
    conn.send("OK@Welcome to the server".encode(FORMAT))
    
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
        
        send_data = "OK@"

        if cmd == "LOGOUT":
            break
        elif cmd == "UPLOAD":
            # code for receiveing a file
        elif cmd == "DELETE":
            # code for deleting a file

        

    print(f"{addr} disconnected")
    conn.close()

def main():
    print("Starting the server")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"server is listening on {IP}: {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()

    if __name__ == "__main__":
        main()