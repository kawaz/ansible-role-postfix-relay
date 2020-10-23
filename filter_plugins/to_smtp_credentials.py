# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import re

def to_smtp_credentials(_password, region=None, relayhost=None, password_conversion_mode=None, **kv):
    if password_conversion_mode == None or password_conversion_mode == "aws_ses_v4":
        return to_smtp_credentials_aws_ses_v4(_password, region, relayhost)
    if password_conversion_mode == "aws_ses_before20190110":
        return to_smtp_credentials_aws_ses_before20190110(_password)
    raise AnsibleFilterError('Invalid value for password_conversion_mode: %s' % password_conversion_mode)

def to_smtp_credentials_aws_ses_before20190110(password):
    return base64.b64encode(chr(2).encode() + hmac.new(password.encode("utf-8"), b"SendRawEmail", hashlib.sha256).digest()).decode()

def hmac_sha256(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def to_smtp_credentials_aws_ses_v4(password, region='us-east-1', relayhost=None):
    if relayhost != None:
        m = re.search('email-smtp\.([a-z0-9-]+)\.amazonaws.com', relayhost)
        if m != None:
            region = m.group(1)
    if region == None:
        region = 'us-east-1'
    signature = hmac_sha256(("AWS4" + password).encode('utf-8'), "11111111")
    signature = hmac_sha256(signature, region)
    signature = hmac_sha256(signature, "ses")
    signature = hmac_sha256(signature, "aws4_request")
    signature = hmac_sha256(signature, "SendRawEmail")
    signatureAndVersion = bytes([0x04]) + signature
    smtpPassword = base64.b64encode(signatureAndVersion)
    return smtpPassword.decode()

class FilterModule(object):
    def filters(self):
        return {
            'to_smtp_credentials': to_smtp_credentials
        }

if __name__ == "__main__":
    import sys
    print(to_smtp_credentials(sys.argv[1], relayhost=sys.argv[2]))
