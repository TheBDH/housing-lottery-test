import tabula
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("liveData")
SNAPSHOT_PREFIX = "spring_room_selection_"


def pdf_to_csv(pdf_path: str, publish_date: str, publish_time: str) -> str:
    """Convert one PDF file into a liveData snapshot CSV and return the CSV path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_file = OUTPUT_DIR / f"{SNAPSHOT_PREFIX}4_{publish_date}_{publish_time}.csv"

    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
    if not tables:
        raise ValueError(f"No tables found in: {pdf_path}")

    combined = pd.concat(tables, ignore_index=True)
    combined.to_csv(csv_file, index=False)
    return str(csv_file)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        raise SystemExit("Usage: python pdfToCSV.py /path/to/file.pdf <publish_date> <publish_time>")

    output_path = pdf_to_csv(sys.argv[1], sys.argv[2], sys.argv[3])
    print(f"Saved: {output_path}")