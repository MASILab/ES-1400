import socket

def send_messages(ip_address, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip_address, port))
        print("Connected to the receiver.")
        while True:
            message = input("Enter the message to send (type 'exit' to quit): ")
            if message.lower() == 'exit':
                print("Closing connection.")
                break
            s.sendall(message.encode())

if __name__ == "__main__":
    ip_address = input("Enter the IP address of the receiving Pi: ")
    port = int(input("Enter the port number: "))
    send_messages(ip_address, port)
