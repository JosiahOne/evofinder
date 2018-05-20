![alt text](
https://raw.githubusercontent.com/JosiahOne/evofinder/master/header.png "Header")
# evofinder

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3ee8fb601041413d9d6bbdc287b86b38)](https://app.codacy.com/app/josiah/evofinder?utm_source=github.com&utm_medium=referral&utm_content=JosiahOne/evofinder&utm_campaign=badger)

evofinder is an evolutionary input fuzzer
(https://en.wikipedia.org/wiki/Fuzzing) for python programs that attempts to
automatically generate inputs to cause the program to reach a pre-specified
target location in the control flow graph
(https://en.wikipedia.org/wiki/Control_flow_graph).

Note: This project was created while at the University of Michigan as a final project for a complex systems course. It is still in active development.

## Motivation & Background

### Static Code Analysis
In computer security, we are often interested in finding software
"vulnerabilities" before deploying the software. One way this is done is by
looking at the source code (called static analysis). Many tools exist to
automatically analyze this code, and will print out *probable* issues.

The reason these issues have to be *probable* and not *certain* is because
it is very computationally difficult (indeed, NP-hard) to prove that certain
things can happen to cause an issue. To combat this, static analysis tools
use conservative estimates. They tend to simplify tasks, but will assume the
"bad" thing if it can't make an accurate-enough judgement.

An example static code analysis tool for python is pyt:
https://github.com/python-security/pyt

### Verifying Static Code Analysis Results
After obtaining a list of potential places in your code where a vulnerability
might exist, it is then desirable to verify that an attacker could actually
create some input to cause the program to reach this part of the control flow
graph. For instance, consider the following (vulnerable) python program:

    import sys
    import os
    
    if sys.argv[1] == "hello":
        os.system(argv[2])
    else:
        print("Need correct argument")
    
    
A static code analysis tool might indicate that the os.system(argv[2]) line
is dangerous because the attack could control what command is executed. However,
we want to then automatically find an input that could cause us to reach that
line in the control flow graph. The control flow graph for this program might
look like:

                            ------------------------------
                            | import sys                 |
                            | import os                  |
                            | if sys.argv[1] == "hello": |
                            ------------------------------
                                         /\
                                FALSE   /  \   TRUE
                                       /    \
                                      /      \
    ----------------------------------        ------------------------
    | print("Need correct argument") |       | os.system(sys.argv[2]) |
    ----------------------------------        ------------------------


So the goal is to find a sys.argv[1] and sys.argv[2] input such that the TRUE
path is taken. This can be done via evoultionary algorithms by modifying the
values of sys.argv (the input parameters to the program). The fitness function
is intuitively how "close" the program actually got to the desired location.

Note: How to determine this is arguably the hardest part of this project.

### Fuzzers

This process of generating inputs to cause some condition to happen is called
"fuzzing" in computer security. Wikipedia has a fairly nice article on it here:
https://en.wikipedia.org/wiki/Fuzzing

A well-known (and useful in the real world) evolutionary fuzzer is called
afl and is available here: http://lcamtuf.coredump.cx/afl/ The technical details
can be found here:
http://lcamtuf.coredump.cx/afl/technical_details.txt

I strongly suggest reading the technical details as this project, at a
high-level evo-finder could be described as:

"afl-fuzz, but for python, and where the goal is to get to a specific location,
not get to as many locations as possible"

## Approach

1. Instrument the program.
2. Create a population of inputs.
3. Run each input and evaluate its fitness (how close it got to the target).
4. Evolve & mutate population

## Presentations
* https://docs.google.com/presentation/d/1aMfXO5Xk7eZcNa6JO5KRX-DYwEcKMtrpEPZvvOZ3FbA/
