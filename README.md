Ansible role for postfix with sender depended relay and sasl authentication
--

[![Build Status](https://travis-ci.com/kawaz/ansible-role-postfix-relay.svg?branch=master)](https://travis-ci.com/kawaz/ansible-role-postfix-relay)
[![Ansible galaxy](https://img.shields.io/badge/ansible--galaxy-kawaz.postfix--relay-blue.svg)](https://galaxy.ansible.com/kawaz/postfix-relay/)

# Requirements

None

# Role Variables

- `postfix_relay_configs_template`: List of configuration template.

# Role Variables

|Variable|Description|Default|
|---|---|---|
|`postfix_relay_configs`|Extra configs of main.cf|`{}`|
|`postfix_relay_maps`|Maps of `{sender, relayhost, username, password, enable_password_conversion_for_ses}`|`[]`|
|`postfix_relay_maps[].sender`|sender. If sender contains `@*.`, it matches subdomains.||
|`postfix_relay_maps[].sender_matches_subdomains`|If this is `yes`, sender matches subdomains. This is the same as including `@*.` in sender.|`no`|
|`postfix_relay_maps[].relayhost`|relayhost||
|`postfix_relay_maps[].username`|sasl username||
|`postfix_relay_maps[].password`|sasl password||
|`postfix_relay_maps[].enable_password_conversion_for_ses`|If this is `yes`, then your normal aws credentials will be converted to ses smtp credentioals. For details, see [here](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html#smtp-credentials-convert)|`no`|
|`postfix_relay_maps[].password_conversion_mode`|Pasword conversion mode used when enable_password_conversion_for_ses is yes. If IAM AccessKey created until 2019-01-10, then use `aws_ses_before20190110` else use `aws_ses_v4`. [see here](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html)|`aws_ses_v4`|
|`postfix_relay_sender_dependent_relayhost_maps`|Maps of relayhost for each sender|`{}`|
|`postfix_relay_smtp_sasl_password_maps`|Maps of `USERNAME:PASSWORD` for each relayhost or sender|`{}`|

# Dependencies

Postfix

# Example Playbook

## AmazonSES (credentials is normal aws credentials, not smtp credentials)
This is simple playbook for AmazonSES.

```yaml
- hosts: servers
  roles:
    - role: kawaz.postfix-relay
      postfix_relay_maps:
        - sender: '@example.com'
          sender_matches_subdomains: yes
          relayhost: '[email-smtp.us-east-1.amazonaws.com]:587'
          username: 'AKIAIOSFODNN7EXAMPLE'
          password: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
          enable_password_conversion_for_ses: yes
```

If your credentials is created by management console, you don't need `enable_password_conversion_for_ses: yes`.

## Multiple identities
This is example for combined multiple identities of AmazonSES and gmail account.

```yaml
- hosts: servers
  roles:
    - role: kawaz.postfix-relay
      postfix_relay_sender_dependent_relayhost_maps:
        '@example.com': '[email-smtp.us-east-1.amazonaws.com]:587'
        '@example.org': '[email-smtp.us-east-1.amazonaws.com]:587'
        '@example.net': '[email-smtp.us-east-1.amazonaws.com]:587'
        '@*.example.info': '[email-smtp.us-east-1.amazonaws.com]:587'
        'user@google.com': '[smtp-relay.gmail.com]:587'
        '@intra.local': '[10.0.0.25]:25'
      postfix_relay_smtp_sasl_password_maps:
        '@example.com': 'AWS_ACCESS_KEY1:AWS_ACCESS_SECRET1'
        '@example.org': 'AWS_ACCESS_KEY2:AWS_ACCESS_SECRET2'
        '@*.example.info': 'AWS_ACCESS_KEY3:AWS_ACCESS_SECRET3'
        '[email-smtp.us-east-1.amazonaws.com]:587': 'AWS_ACCESS_KEY4:AWS_ACCESS_SECRET4'
        'user@google.com': 'user@google.com:PASSWORD'
      postfix_relay_maps:
        - sender: '@example.jp'
          relayhost: '[smtp-relay.gmail.com]:587'
        - sender: '@*.example.jp'
          relayhost: '[smtp-relay.gmail.com]:587'
        - sender: 'foo@example.jp'
          username: 'foo@example.jp'
          password: 'FOOPASSWORD'
        - sender: 'bar@example.jp'
          username: 'bar@example.jp'
          password: 'BARPASSWORD'
```

# License

MIT

# Author Information

Yoshiaki Kawazu
