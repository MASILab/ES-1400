import socket

def receive_messages(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()
        print(f"Listening on port {port}...")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    print("Connection closed by the sender.")
                    break
                print('Received message:', data.decode())

if __name__ == "__main__":
    port = int(input("Enter the port number to listen on: "))
    receive_messages(port)
