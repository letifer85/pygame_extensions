from __future__ import annotations

import pytest

test_cases = [
    (0, 0)
]


@pytest.mark.parametrize('param, expected', test_cases)
def test_(
    param, expected
):
    assert param == expected


def test_exception():
    with pytest.raises(Exception, match=r''):
        raise Exception('Test not implemented')
