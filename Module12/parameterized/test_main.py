import pytest

@pytest.mark.parametrize("number, expected", [
    (2, 4),
    (3, 9),
    (5, 25),
])
def test_square(number, expected):
    assert number ** 2 == expected