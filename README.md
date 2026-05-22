# pdf2anki

Create an Anki-ready CSV (Front,Back) from text extracted from a PDF.

## Usage

```bash
pip install pypdf
python pdf2anki.py input.pdf output.csv
```

By default, each non-empty line is split into `Front` and `Back` using `" - "`.
If a line does not contain the separator, it is exported with an empty `Back` field.

Use a custom separator when needed:

```bash
python pdf2anki.py input.pdf output.csv --separator ";"
```
