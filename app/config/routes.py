from lib.response import Response
from endpoints.file import File

routes = {
            "GET": {
                "/echo/(characters)": lambda request: Response(body=request.props['characters']),
                "/user-agent": lambda request: Response(body=request.headers['User-Agent']),
                "/files/(filename)": (File, "get_file"),
                "/": lambda request: Response(body="root")
            },
            "POST": {
                "/files/(filename)": (File, "create_file"),
            }
            
        }