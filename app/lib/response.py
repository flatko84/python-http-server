from dataclasses import dataclass, field

@dataclass
class Response:
    headers: dict = field(default_factory=lambda: {})
    body: str = field(default="")
    status: str = field(default="200 OK")

    def __post_init__(self) -> None:
        """Massage headers after instantiation."""
        if "Content-Type" not in self.headers.keys():
            self.headers['Content-Type'] = "text/plain"


    def get_header(self, header) -> str | None:
        """Return a header content by header name or None if the header is not set."""
        if header not in self.headers.keys():
            return None
        return self.headers[header]

    @property
    def full_headers(self) -> dict:
        """Massage headers before sending response."""
        full_headers = self.headers.copy()
        full_headers['Content-Length'] = len(self.body)
        return full_headers
    
    def __str__(self) -> str:
        """Format the response to string before sending."""
        headers_string = "".join([f"{header}: {content}\r\n" for header, content in self.full_headers.items()])
        return f"HTTP/1.1 {self.status}\r\n{headers_string}\r\n{self.body}"
    