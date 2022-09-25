import pytest


class TestExShortPhrase:
    def setup(self):
        self.phrase = input("\nSet a phrase with len < 15: ")

    def test_ex_short_phrase(self):
        assert len(self.phrase) < 15, f'len (phrase) >= 15'
