
import json

class R:
    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data

    @staticmethod
    def success(data=None):
        r = R(0, "success", data)
        return r

    @staticmethod
    def failed(msg, code=-1):
        r = R(code, msg, None)
        return r

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) 