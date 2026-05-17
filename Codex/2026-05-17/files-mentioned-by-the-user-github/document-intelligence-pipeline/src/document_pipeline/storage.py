from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import DocumentRecord


class LocalStorageWriter:
    CSV_FIELDS = [
        "source_file",
        "document_id",
        "supplier",
        "invoice_date",
        "due_date",
        "purchase_order",
        "department",
        "cost_center",
        "currency",
        "net_amount",
        "tax_amount",
        "total_amount",
        "extraction_confidence",
        "status",
        "issue_count",
    ]

    def write(self, records: list[DocumentRecord], output_dir: Path) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)

        csv_path = output_dir / "extracted_documents.csv"
        json_path = output_dir / "extracted_documents.json"
        exception_path = output_dir / "exceptions.csv"

        self._write_csv(records, csv_path)
        self._write_json(records, json_path)
        self._write_exceptions(records, exception_path)

        return [csv_path, json_path, exception_path]

    def _write_csv(self, records: list[DocumentRecord], path: Path) -> None:
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.CSV_FIELDS)
            writer.writeheader()
            for record in records:
                row = record.to_dict()
                writer.writerow({field: row[field] for field in self.CSV_FIELDS})

    def _write_json(self, records: list[DocumentRecord], path: Path) -> None:
        payload = [record.to_dict() for record in records]
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _write_exceptions(self, records: list[DocumentRecord], path: Path) -> None:
        rows = []
        for record in records:
            if record.status != "needs_review":
                continue
            for issue in record.issues:
                rows.append(
                    {
                        "source_file": record.source_file,
                        "document_id": record.document_id,
                        "supplier": record.supplier,
                        "field": issue.field,
                        "severity": issue.severity,
                        "message": issue.message,
                    }
                )

        with path.open("w", encoding="utf-8", newline="") as file:
            fieldnames = [
                "source_file",
                "document_id",
                "supplier",
                "field",
                "severity",
                "message",
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

