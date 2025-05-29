from endpoints.endpoint import Endpoint
from lib.response import Response

class File(Endpoint):
    def get_file(self):
        try:
            # to do - set this dynamically from the shell script
            with open(f"../storage/{self.request.props['filename']}") as file:
                body = file.read()
            response = Response(body=body)
            response.headers["Content-Type"] = "application/octet-stream"
            return response
        except:
            return Response(status="404 Not Found")
        
    def create_file(self):
        with open(f"../storage/{self.request.props['filename']}", "w") as file:
            file.write(self.request.body)
        return Response(status="201 Created")