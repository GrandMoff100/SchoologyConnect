import base64
import time

make_cookie = lambda: base64.b64encode(
        str(
            time.time()
        ).encode('utf-8')
    ).decode('utf-8')