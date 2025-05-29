from lib.request import Request
from webapp.router import Router
from hooks.hooks import Hooks

class Connection:

    def build_request(self, data):
        print(data)
        head, body = data.split("\r\n\r\n")
        head_parsed = head.split("\r\n")
        method, route, protocol = head_parsed[0].split(" ")
        props = {}
        headers = {}
        if (len(head_parsed)) > 1:
            for header_row in head_parsed[1:]:
                header_row_split = header_row.split(": ")
                headers[header_row_split[0]] = header_row_split[1]
        return Request(method=method, route=route, protocol=protocol, props=props, headers=headers, body=body)


    def connect(self, socket_object, ret_address):
            with socket_object:
                buffer = b""
                hooks = Hooks()
                while True:
                    try:
                        received_data = socket_object.recv(1024)
                        buffer += received_data
                    except:
                        print("Error reading request.")
                    if len(received_data) == 0:
                        break
                    request_data = buffer.decode()
                    if '\r\n\r\n' not in request_data:
                        continue
                    request = self.build_request(request_data)
                    request = hooks.receive(request)
                    response = Router(request).route()
                    response = hooks.send(request, response)
                    if 'Connection' in request.headers.keys() and request.headers["Connection"].lower() == 'close':
                        response.headers["Connection"] = "close"
                    socket_object.sendall(response.text.encode())
                    buffer = b""
                