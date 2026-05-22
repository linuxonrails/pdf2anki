import csv
import tempfile
import unittest
from pathlib import Path

from pdf2anki import convert_lines_to_rows, write_rows_to_csv


class Pdf2AnkiTests(unittest.TestCase):
    def test_convert_lines_to_rows_splits_on_separator(self):
        rows = convert_lines_to_rows(
            [
                "hello - hola",
                "goodbye - adios",
                "single side",
                "",
                "  spaced - separado  ",
            ],
            " - ",
        )

        self.assertEqual(
            rows,
            [
                ("hello", "hola"),
                ("goodbye", "adios"),
                ("single side", ""),
                ("spaced", "separado"),
            ],
        )

    def test_write_rows_to_csv_writes_two_columns(self):
        rows = [("front 1", "back 1"), ("front 2", "")]
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "anki.csv"
            write_rows_to_csv(rows, output)

            with output.open(newline="", encoding="utf-8") as csv_file:
                reader = list(csv.reader(csv_file))

        self.assertEqual(reader, [["front 1", "back 1"], ["front 2", ""]])


if __name__ == "__main__":
    unittest.main()
