# Ansible [kawaz.postfix-relay](https://galaxy.ansible.com/kawaz/postfix-relay/) role

[![Build Status](https://travis-ci.org/kawaz/ansible-role-postfix-relay.svg?branch=master)](https://travis-ci.org/kawaz/ansible-role-postfix-relay)

Ansible role for postfix with sender depended relay and sasl authentication

# Requirements

None

# Role Variables

- `postfix_relay_configs_template`: List of configuration template.

# Role Variables

|Variable|Description|Default|
|---|---|---|
|`postfix_relay_configs`|Extra configs of main.cf|`{}`|
|`postfix_relay_sender_dependent_relayhost_maps`|Maps of relayhost for each sender|`{}`|
|`postfix_relay_smtp_sasl_password_maps`|Maps of `USERNAME:PASSWORD` for each relayhost or sender|`{}`|
|`postfix_relay_maps`|Maps of `{sender, relayhost, password, enable_password_conversion_for_ses}`|`{}`|

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
        sender: '@example.com'
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
        'user@google.com': '[smtp-relay.gmail.com]:587'
      postfix_relay_smtp_sasl_password_maps:
        '@example.com': 'AWS_ACCESS_KEY1:AWS_ACCESS_KEY1'
        '@example.org': 'AWS_ACCESS_KEY2:AWS_ACCESS_KEY2'
        'user@google.com': 'user@google.com:PASSWORD'
        '[extra-relay.example.com]:587': 'USERNAME:PASSWORD'
```

# License

MIT

# Author Information

Yoshiaki Kawazu
