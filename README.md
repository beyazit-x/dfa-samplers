# dfa-sampler
Library for implementing dfa sampling strategies (pull requests welcome).

[![PyPI version](https://badge.fury.io/py/dfa-sampler.svg)](https://badge.fury.io/py/dfa-sampler)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Installation

If you just need to use `dfa-sampler`, you can just run:

`$ pip install dfa-sampler`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

The `dfa` api is centered around the `DFA` object. 

By default, the `DFA` object models a `Deterministic Finite Acceptor`,
e.g., a recognizer of a Regular Language. 


```python
from dfa_sampler import gen_reach_avoid, gen_mutated_reach_avoid

dfas1 = gen_reach_avoid(n_tokens=3)
dfas2 = gen_mutated_reach_avoid(n_tokens=12)
```
