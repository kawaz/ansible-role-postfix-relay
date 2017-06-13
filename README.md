# Ansible postfix-relay role

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
|`postfix_relay_maps`|Maps of `{sender, relayhost, password}`|`{}`|

# Dependencies

Postfix

# Example Playbook

This is simple playbook for AmazonSES.

```yaml
- hosts: servers
  roles:
    - role: kawaz.postfix-relay
      postfix_relay_maps:
        sender: '@example.com'
        relayhost: '[email-smtp.us-east-1.amazonaws.com]:587'
        password: 'AWS_ACCESS_KEY:AWS_ACCESS_SECRET'
```

This is example for combined multiple domains of AmazonSES and gmail account.

```yaml
- hosts: servers
  roles:
    - role: kawaz.postfix-relay
      postfix_relay_sender_dependent_relayhost_maps:
        '@example.com': '[email-smtp.us-east-1.amazonaws.com]:587'
        '@example.org': '[email-smtp.us-east-1.amazonaws.com]:587'
        'user@google.com': '[smtp-relay.gmail.com]:587'
      postfix_relay_smtp_sasl_password_maps:
        '@example.com': 'AWS_ACCESS_KEY1:AWS_ACCESS_SECRET1'
        '@example.org': 'AWS_ACCESS_KEY2:AWS_ACCESS_SECRET2'
        'user@google.com': 'user@google.com:PASSWORD'
        '[extra-relay.example.com]:587': 'USERNAME:PASSWORD'
```

# License

MIT

# Author Information

Yoshiaki Kawazu
