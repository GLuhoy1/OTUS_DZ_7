import socket
import re
from http import HTTPStatus

HOST = '192.168.44.153'
PORT = 8087

BROWSERS = ['Mozilla', 'Chrome', 'Safari', 'Edge', 'Opera']


def parse_request_status_code(request):
    http_method = 'GET'
    http_status = HTTPStatus.OK
    status_match = re.search(r'\/\?status=(\d+)', request)
    if status_match:
        status_code = int(status_match.group(1))
        try:
            http_status = HTTPStatus(status_code)
        except ValueError:
            pass

    return http_method, http_status


def parse_request_headers(request):
    headers = {}
    lines = request.split('\r\n')
    for line in lines[1:]:
        if line:
            header_name, header_value = line.split(': ', 1)
            headers[header_name] = header_value
    return headers


def generate_response(http_method, client_address, http_status, accepted_request_headers):
    result = f"Request Method: {http_method}\n"
    result += f"Request Source: {client_address[0]}:{client_address[1]}\n"
    result += f"Response Status: {http_status.value} {http_status.phrase}\n"

    for header_name, header_value in accepted_request_headers.items():
        result += f"{header_name}: {header_value}\n"

    return result


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    srv_addr = (HOST, PORT)
    s.bind(srv_addr)
    s.listen(1)
    print(f'Server start on: {HOST}:{PORT}')

    while True:
        print('Waiting for a new connection')

        conn, raddr = s.accept()
        print(f'Connection from {raddr}')

        data = conn.recv(2048)
        text = data.decode('utf-8')

        if text:
            method, status = parse_request_status_code(text)
            request_headers = parse_request_headers(text)
            response = generate_response(method, raddr, status, request_headers)

            conn.send(response.encode('utf-8'))
        else:
            break

        conn.close()
