import socket
from threading import Thread
import gzip

# could be a dataclass in a real-world app
class Request:
    def __init__(self, data):
        self.head, self.body = data.split("\r\n\r\n")
        head_parsed = self.head.split("\r\n")
        self.method, self.route, self.protocol = head_parsed[0].split(" ")
        self.props = {}
        self.headers = {}
        if (len(head_parsed)) > 1:
            for header_row in head_parsed[1:]:
                header_row_split = header_row.split(": ")
                self.headers[header_row_split[0]] = header_row_split[1]

    def __repr__(self):
        return f"(method='{self.method}' route='{self.route}' protocol='{self.protocol}' headers='{"".join([f"{header}: {value}" for header, value in self.headers.items()])}' body='{self.body}')"

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
    
    # must be in a separate place for endpoints
    def get_file(self, request):
        try:
            # to do - set this dynamically from the shell script
            with open(f"storage/{request.props['filename']}") as file:
                body = file.read()
            response = Response(body=body)
            response.add_header("Content-Type", "application/octet-stream")
            return response
        except:
            return Response(status="404 Not Found")
        
    def create_file(self, request):
        with open(f"storage/{request.props['filename']}", "w") as file:
            file.write(request.body)
        return Response(status="201 Created")
        

# to do - separate file for the dictionary and anoher one for the routing logic, possibly incorporating the path_match method    
    def router(self, request):
        routes = {
            "GET": {
                "/echo/(characters)": lambda request: Response(body=request.props['characters']),
                "/user-agent": lambda request: Response(body=request.headers['User-Agent']),
                "/files/(filename)": self.get_file,
                "/": lambda request: Response(body="root")
            },
            "POST": {
                "/files/(filename)": self.create_file,
            }
            
        }
        # to do - try except
        for route, endpoint in routes[request.method].items():
            props = self.path_match(request.route, route)
            if type(props) == dict:
                request.props = props
                return endpoint(request)
        return Response(status="404 Not Found")
    
    def gzip_compress(self, content):
        return gzip.compress(content.encode())

    def compress(self, header, content):
        supported_compressions = {
            'gzip': self.gzip_compress
        }
        compressions = header.split(" ,")
        for compression in compressions:
            if compression in supported_compressions.keys():
                return (compression, supported_compressions[compression](content))
        return (False, content)
    

# to do - split and eventually decouple web app from server
    def serve(self, socket_object, ret_address):
        with socket_object:
            request_data = socket_object.recv(1024).decode()
            request = Request(request_data)
            print(request)
            response = self.router(request)
            # to do - implement middleware
            try:
                compression_header, request.body = self.compress(request.headers["Accept-Encoding"], request.body)
                if compression_header:
                    response.add_header("Content-Encoding", compression_header)
            except:
                print("No compression used.")
            socket_object.sendall(response.prepare.encode())

# to do - must be a separate file
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
