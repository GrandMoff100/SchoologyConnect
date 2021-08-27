import base64
import time


def make_cookie():
    return base64.b64encode(
        str(
            time.time()
        ).encode('utf-8')
    ).decode('utf-8')
