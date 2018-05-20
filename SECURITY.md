# Security
This document describes the security-relevant aspects of evofinder. This
includes a definition of our attacker model, current risk assessment,
planned (or implemented) countermeasures, and vulnerability disclosure policy.

## Attacker Model
  1. Attacker is smart (e.g. Nation-State)
  2. Attacker has signficant resources (computational, money, memory, etc.)
  3. Attacker is interested in compromising any of confidentiality, integrity, or authenticity of data/machine.
  4. Attacker can control contents of files evofinder *reads*.
  5. Attacker can not change arguments passed to evofinder/python. (i.e. we don't care about external shell attacks)


## Risk Assessment
...

## Countermeasures
...

## Vulnerability Disclosure Policy
evofinder generally does not exist on production machines and we therefore opt
to follow an open disclosure policy. If you find any security vulnerabilities,
please file them directly on the issue tracker and add the "security" label.

This document will list all resolved vulnerabilities.

### Vulnerbability List
N/A
