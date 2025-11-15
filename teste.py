import pytest

def calc(x):
    return (x+1)

def somaResult():
    assert calc(2) == 3