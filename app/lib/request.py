from dataclasses import dataclass

@dataclass
class Request:
    method: str
    route: str
    protocol: str
    headers: dict
    props: dict
    body: str
