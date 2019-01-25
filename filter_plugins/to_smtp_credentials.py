# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac


def to_smtp_credentials(aws_secret):
    return base64.b64encode(chr(2).encode() + hmac.new(aws_secret.encode("utf-8"), b"SendRawEmail", hashlib.sha256).digest()).decode()


class FilterModule(object):
    def filters(self):
        return {
            'to_smtp_credentials': to_smtp_credentials
        }
