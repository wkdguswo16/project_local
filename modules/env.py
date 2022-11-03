import json
from types import SimpleNamespace
def jsonObj(direct) -> object:
    return json.loads(direct, object_hook=lambda d: SimpleNamespace(**d))
ENV = jsonObj(open('secret_key.json', 'r').read())