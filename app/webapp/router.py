from lib.response import Response
from config.routes import routes

class Router:
    def __init__(self, request):
        self.request = request

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
        
    def route(self):
        for route, endpoint in routes[self.request.method].items():
            props = self.path_match(self.request.route, route)
            if type(props) == dict:
                self.request.props = props
                if type(endpoint) == tuple:
                    cls, method_name = endpoint
                    return getattr(cls(self.request), method_name)()
                return endpoint(self.request)
        return Response(status="404 Not Found")