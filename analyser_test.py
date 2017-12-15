import pytest
from analyser import *


@pytest.mark.parametrize("symbol, expected", [
    (Symbol("00", 10), SequenceResult(None, None)),
    (Symbol("01", 10), SequenceResult(None, None)),
    (Symbol("10", 10), SequenceResult(None, None)),
    (Symbol("11", 10), SequenceResult(None, None))
])
def test_add_first_symbol_to_sequence(symbol, expected):
    sequence = Sequence()
    assert sequence.add_and_analyse(symbol) == expected


@pytest.mark.parametrize("symbol_list, expected", [
    ([Symbol("00", 10), Symbol("01", 11), Symbol("11", 12)], SequenceResult(False, -11)),
    ([Symbol("00", 10), Symbol("10", 13), Symbol("11", 12)], SequenceResult(False, 13)),
    ([Symbol("11", 10), Symbol("01", 14), Symbol("00", 12)], SequenceResult(False, 14)),
    ([Symbol("11", 10), Symbol("10", 15), Symbol("00", 12)], SequenceResult(False, -15)),
])
def test_add_valid_delay(symbol_list, expected):
    sequence = Sequence()
    for symbol in symbol_list[:-1]:
        sequence.add_and_analyse(symbol)

    assert sequence.add_and_analyse(symbol_list[-1]) == expected
    assert len(sequence.list) == 1
    assert sequence.list[0] == symbol_list[-1]


@pytest.mark.parametrize("symbol_list, expected", [
    ([Symbol("00", 10), Symbol("11", 11)], SequenceResult(False, 0)),
    ([Symbol("11", 10), Symbol("00", 13)], SequenceResult(False, 0)),
])
def test_add_instantaneous_delay(symbol_list, expected):
    sequence = Sequence()
    for symbol in symbol_list[:-1]:
        sequence.add_and_analyse(symbol)

    assert sequence.add_and_analyse(symbol_list[-1]) == expected
    assert len(sequence.list) == 1
    assert sequence.list[0] == symbol_list[-1]


@pytest.mark.parametrize("symbol_list, expected", [
    ([Symbol("00", 10), Symbol("01", 11), Symbol("10", 11), Symbol("11", 12)], SequenceResult(True, None)),
    ([Symbol("00", 10), Symbol("10", 13), Symbol("01", 11), Symbol("11", 12)], SequenceResult(True, None)),
    ([Symbol("11", 10), Symbol("01", 14), Symbol("10", 11), Symbol("00", 12)], SequenceResult(True, None)),
    ([Symbol("11", 10), Symbol("10", 15), Symbol("01", 11), Symbol("00", 12)], SequenceResult(True, None)),
])
def test_add_invalid_delay(symbol_list, expected):
    sequence = Sequence()
    for symbol in symbol_list[:-1]:
        sequence.add_and_analyse(symbol)

    assert sequence.add_and_analyse(symbol_list[-1]) == expected
    assert len(sequence.list) == 1
    assert sequence.list[0] == symbol_list[-1]


@pytest.mark.parametrize("symbol_list, expected", [
    ([Symbol("00", 10), Symbol("00", 11)], 21),
    ([Symbol("00", 10), Symbol("10", 13), Symbol("10", 11)], 24),
    ([Symbol("11", 10), Symbol("01", 14), Symbol("00", 11), Symbol("00", 12)], 23),
])
def test_add_repeated_symbols(symbol_list, expected):
    sequence = Sequence()
    for symbol in symbol_list:
        sequence.add_and_analyse(symbol)

    assert sequence.list[-1].duration == expected