from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from document_pipeline.pipeline import DocumentPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the document intelligence pipeline."
    )
    parser.add_argument(
        "--input-dir",
        default="data/samples",
        help="Folder containing sample document text files.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Folder where CSV, JSON, and dashboard outputs are written.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pipeline = DocumentPipeline(
        input_dir=PROJECT_ROOT / args.input_dir,
        output_dir=PROJECT_ROOT / args.output_dir,
    )
    summary = pipeline.run()

    print("Document Intelligence Pipeline")
    print(f"Processed documents: {summary.total_documents}")
    print(f"Approved: {summary.approved_documents}")
    print(f"Needs review: {summary.exception_documents}")
    print(f"Total approved value: {summary.currency} {summary.approved_value:,.2f}")
    print("Output files:")
    for path in summary.output_files:
        print(f"- {path}")


if __name__ == "__main__":
    main()

