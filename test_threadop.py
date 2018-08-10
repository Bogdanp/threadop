import operator

import pytest

from threadop import enable_threadop


def test_threadop_rewrites_functions():
    @enable_threadop
    def example():
        return 42 | operator.add(2) | operator.mul(5)

    assert example() == 220


def test_threadop_fails_if_rhs_is_not_a_fn_call():
    with pytest.raises(RuntimeError):
        @enable_threadop
        def example():
            return 42 | operator.add
