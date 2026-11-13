import unittest
from datetime import date

from tennisage.data import _process_career_js


FEMALE_JS = """var morematchmx = [
["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "", "", "", "", "Anne Miller", "", "", "", "", "19770119"]
];"""

MALE_JS = """var morematchmx = [
["20010910", "Spain F10", "Hard", "S", "L", "", "", "", "", "", "", "Guillermo Platel", "", "", "", "", "22.264202601"]
];"""


class ProcessingTests(unittest.TestCase):
    def test_female_file_converts_opponent_birth_date_to_age(self):
        data = _process_career_js(FEMALE_JS, date(1981, 9, 26))
        self.assertEqual(len(data), 1)
        self.assertAlmostEqual(data.loc[0, "opponent_age"], 18.78, places=1)
        self.assertEqual(data.loc[0, "result"], "L")

    def test_male_file_keeps_decimal_opponent_age(self):
        data = _process_career_js(MALE_JS, date(1986, 6, 3))
        self.assertAlmostEqual(data.loc[0, "opponent_age"], 22.264202601)
        self.assertEqual(data.loc[0, "result"], "L")

    def test_unreadable_js_returns_a_clear_error(self):
        with self.assertRaisesRegex(ValueError, "morematchmx"):
            _process_career_js("var something_else = [];", date(1981, 9, 26))


if __name__ == "__main__":
    unittest.main()
