import gzip
from hooks.send_abc import SendABC
from lib.request import Request
from lib.response import Response

class Compression(SendABC):

    def gzip_compress(self, content: str):
        """Compress content using GZIP."""
        return gzip.compress(content.encode())

    def compress(self, header: str, content: str) -> tuple:
        """Match the supported compression formats and compress the content."""
        supported_compressions = {
            'gzip': self.gzip_compress
        }
        compressions = header.split(" ,")
        for compression in compressions:
            if compression in supported_compressions.keys():
                return (compression, supported_compressions[compression](content))
        return (False, content)
    
    def handle(self, request: Request, response: Response) -> Response:
        """The entry point of the hook."""
        try:
            compression_header, request.body = self.compress(request.headers["Accept-Encoding"], request.body)
            if compression_header:
                response.headers["Content-Encoding"] = compression_header
        except:
            print("No compression used.")
        return response