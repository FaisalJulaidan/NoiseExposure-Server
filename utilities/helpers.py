import json

def jsonResponse(success: bool, http_code: int, msg: str, data=None):
    return json.dumps({'success': success, 'code': http_code, 'msg': msg, 'data': data}), \
           http_code, {'ContentType': 'application/json'}

class Callback():
    def __init__(self, success: bool, message: str, data: str or dict or bool = None):
        self.Success: bool = success
        self.Message: str = message
        self.Data: str or dict or bool = data