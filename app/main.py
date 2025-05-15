import socket
from threading import Thread

class Request:
    def __init__(self, data):
        parsed_data = data.split("\r\n")
        print(parsed_data)
        parsed_head = parsed_data[0].split(" ")
        self.method = parsed_head[0]
        self.route = parsed_head[1]
        self.host = parsed_data[1][6:]
        self.user_agent = parsed_data[2][12:]

class Response:
    def __init__(self, body = '', status = "200 OK"):
        self.headers = {"Content-Type": 'text/plain'}
        self.body = body
        self.status = status

    def add_header(self, header, content):
        self.headers[header] = content

    def get_header(self, header):
        if header not in self.headers.keys():
            return None
        return self.headers[header]

    @property
    def full_headers(self):
        full_headers = self.headers.copy()
        full_headers['Content-Length'] = len(self.body)
        return full_headers
    
    @property
    def prepare(self):
        headers_string = " ".join([f"{header}: {content}\r\n" for header, content in self.full_headers.items()])
        return f"HTTP/1.1 {self.status}\r\n{headers_string}\r\n{self.body}"


class HttpServer:
        
    @staticmethod
    def path_match(path, route):
        path_split = path[1:].split("/")
        route_split = route[1:].split("/")
        props_dict = {}
        if len(path_split) != len(route_split):
            return False
        for idx, part in enumerate(route_split):
            if not len(part):
                return False
            if part[0] == '(' and part[-1] == ')':
                props_dict[part[1:-1]] = path_split[idx]
            elif part != path_split[idx]:
                return False
        return props_dict
    
    def get_file(self, props):
        try:
            with open(f"storage/{props['filename']}") as file:
                body = file.read()
            response = Response(body=body)
            response.add_header("Content-Type", "application/octet-stream")
            return response
        except:
            return Response(status="404 Not Found")
        
    def router(self, path, request):
        routes = {
            "/echo/(characters)": lambda props: Response(body=props['characters']),
            "/user-agent": lambda props: Response(body=request.user_agent),
            "/files/(filename)": self.get_file,
            "/": lambda props: Response(body="root")
        }
        for route, endpoint in routes.items():
            match = self.path_match(path, route)
            if type(match) == dict:
                return endpoint(match)
        return Response(status="404 Not Found")

    def serve(self, socket_object, ret_address):
        with socket_object:
            request_data = socket_object.recv(1024).decode()
            request = Request(request_data)
            response = self.router(request.route, request)
            socket_object.sendall(response.prepare.encode())

    def main(self, *args):
        print("Server started.")
        server = socket.create_server(("localhost", 4221), reuse_port=True)
        try:
            while True:
                socket_object, ret_address = server.accept()
                Thread(target=self.serve, args=(socket_object, ret_address)).start()
        except KeyboardInterrupt:
            print("Server stopped.")


if __name__ == "__main__":
    srv = HttpServer()
    srv.main()
