# -*- coding: utf-8 -*-
from ansible import errors
import base64
import hashlib
import hmac

def to_smtp_credentials(aws_secret):
    return base64.b64encode(chr(2) + hmac.new(str(aws_secret), "SendRawEmail", hashlib.sha256).digest())

class FilterModule(object):
    def filters(self):
        return {
            'to_smtp_credentials': to_smtp_credentials
        }
