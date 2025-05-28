import gzip
from hooks.send_abc import SendABC

class Compression(SendABC):

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
    
    def handle(self, request, response):
        try:
            compression_header, request.body = self.compress(request.headers["Accept-Encoding"], request.body)
            if compression_header:
                response.headers["Content-Encoding"] = compression_header
        except:
            print("No compression used.")
        return response