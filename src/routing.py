from fastapi.routing import APIRoute
from pyheck import upper_camel


def generate_unique_route_id(route: APIRoute):
    return upper_camel(route.name)
