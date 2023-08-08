import socket

HOST = '192.168.44.153'
PORT = 8087

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    status_code = 2545
    custom_headers = {
        'Custom-Header1': 'Value1',
        'Custom-Header2': 'Value2'
    }
    headers_str = "\r\n".join([f"{name}: {value}" for name, value in custom_headers.items()])
    request = f"GET /?status={status_code} HTTP/1.1\r\nHost: localhost\r\n{headers_str}\r\n\r\n"

    client_socket.sendall(request.encode())

    response = client_socket.recv(4096)

    print(response.decode())
