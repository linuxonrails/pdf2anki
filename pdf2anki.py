from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


def extract_lines_from_pdf(pdf_path: Path) -> List[str]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - import guard
        raise RuntimeError(
            "Missing dependency 'pypdf'. Install it with: pip install pypdf"
        ) from exc

    reader = PdfReader(str(pdf_path))
    lines: List[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        for raw_line in page_text.splitlines():
            line = raw_line.strip()
            if line:
                lines.append(line)
    return lines


def convert_lines_to_rows(lines: Iterable[str], separator: str) -> List[Tuple[str, str]]:
    rows: List[Tuple[str, str]] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if separator and separator in line:
            front, back = line.split(separator, 1)
            rows.append((front.strip(), back.strip()))
        else:
            rows.append((line, ""))
    return rows


def write_rows_to_csv(rows: Sequence[Tuple[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for front, back in rows:
            writer.writerow([front, back])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert PDF text into an Anki-ready CSV file (Front,Back)."
    )
    parser.add_argument("pdf_file", type=Path, help="Path to source PDF file")
    parser.add_argument("csv_file", type=Path, help="Path to output CSV file")
    parser.add_argument(
        "--separator",
        default=" - ",
        help="Separator used to split each text line into front/back (default: ' - ')",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.pdf_file.exists():
        parser.error(f"Input PDF does not exist: {args.pdf_file}")

    lines = extract_lines_from_pdf(args.pdf_file)
    rows = convert_lines_to_rows(lines, args.separator)
    write_rows_to_csv(rows, args.csv_file)

    print(f"Created {args.csv_file} with {len(rows)} cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
