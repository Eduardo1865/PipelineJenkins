import pytest

def calc(x):
    return (x+1)

def test_somaResult():
    assert calc(2) == 3