import hashlib
import time
import uuid


def createVerificationData():
    stime = str(round(time.time()))
    nonce = str(uuid.uuid4())
    sign = hashlib.md5((str('123456') + nonce + stime).encode()).hexdigest().upper()
    return {
        'stime': stime,
        'nonce': nonce,
        'sign': sign
    }
