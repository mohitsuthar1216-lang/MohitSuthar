from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .dashboard import render_dashboard
from .extractor import RegexInvoiceExtractor
from .models import DocumentRecord
from .storage import LocalStorageWriter
from .validator import DocumentValidator


@dataclass
class PipelineSummary:
    total_documents: int
    approved_documents: int
    exception_documents: int
    approved_value: float
    currency: str
    output_files: list[Path]


class DocumentPipeline:
    def __init__(
        self,
        input_dir: Path,
        output_dir: Path,
        extractor: RegexInvoiceExtractor | None = None,
        validator: DocumentValidator | None = None,
        storage: LocalStorageWriter | None = None,
    ) -> None:
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.extractor = extractor or RegexInvoiceExtractor()
        self.validator = validator or DocumentValidator()
        self.storage = storage or LocalStorageWriter()

    def run(self) -> PipelineSummary:
        records = self._process_documents()
        output_files = self.storage.write(records, self.output_dir)
        dashboard_path = render_dashboard(records, self.output_dir)
        output_files.append(dashboard_path)

        approved_records = [
            record for record in records if record.status == "approved"
        ]
        currency = records[0].currency if records else "EUR"

        return PipelineSummary(
            total_documents=len(records),
            approved_documents=len(approved_records),
            exception_documents=len(records) - len(approved_records),
            approved_value=sum(record.total_amount for record in approved_records),
            currency=currency,
            output_files=output_files,
        )

    def _process_documents(self) -> list[DocumentRecord]:
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input folder not found: {self.input_dir}")

        records = []
        for path in sorted(self.input_dir.glob("*.txt")):
            extracted = self.extractor.extract(path)
            validated = self.validator.validate(extracted)
            records.append(validated)
        return records

