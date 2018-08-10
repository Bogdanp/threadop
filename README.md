# threadop

Adds a threading operator to Python.  This is stupid and you probably shouldn't use it.

Limitations:

* The right-hand side **must** be a function call.
* Requires access to functions' source code.  Meaning this won't work
  in the interpreter.

## Installation

    pip install threadop

## Usage

``` python
import operator

from threadop import enable_threadop


@enable_threadop
def example():
    # The below is equivalent to
    # print(operator.mul(operator.add(42, 15), 2))
    42 | operator.add(15) | operator.mul(2) | print()

example()
```

## License

threadop is licensed under the 3-Clause BSD license.  Please see
[LICENSE] for licensing details.

[LICENSE]: https://github.com/Bogdanp/theradop/blob/master/LICENSE
