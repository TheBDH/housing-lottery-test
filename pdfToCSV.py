import tabula
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("liveData")


def pdf_to_csv(pdf_path: str) -> str:
    """Convert one PDF file to one CSV file and return the CSV path."""
    pdf_file = Path(pdf_path)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_file = OUTPUT_DIR / f"{pdf_file.stem}.csv"

    tables = tabula.read_pdf(str(pdf_file), pages="all", multiple_tables=True)
    if not tables:
        raise ValueError(f"No tables found in: {pdf_file}")

    combined = pd.concat(tables, ignore_index=True)
    combined.to_csv(csv_file, index=False)
    return str(csv_file)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python pdfToCSV.py /path/to/file.pdf")

    output_path = pdf_to_csv(sys.argv[1])
    print(f"Saved: {output_path}")