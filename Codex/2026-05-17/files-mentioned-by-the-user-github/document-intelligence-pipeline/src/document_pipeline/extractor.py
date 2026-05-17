from __future__ import annotations

import re
from pathlib import Path

from .models import DocumentRecord


class RegexInvoiceExtractor:
    """Small local extractor that mimics an enterprise document AI layer."""

    FIELD_PATTERNS = {
        "document_id": r"Invoice No:\s*(?P<value>[A-Z0-9-]+)",
        "supplier": r"Supplier:\s*(?P<value>.+)",
        "invoice_date": r"Invoice Date:\s*(?P<value>\d{4}-\d{2}-\d{2})",
        "due_date": r"Due Date:\s*(?P<value>\d{4}-\d{2}-\d{2})",
        "purchase_order": r"Purchase Order:\s*(?P<value>[A-Z0-9-]+)",
        "department": r"Department:\s*(?P<value>.+)",
        "cost_center": r"Cost Center:\s*(?P<value>[A-Z0-9-]+)",
    }

    AMOUNT_PATTERNS = {
        "net_amount": r"Net Amount:\s*(?P<currency>[A-Z]{3})\s*(?P<value>[\d,]+\.\d{2})",
        "tax_amount": r"Tax Amount:\s*(?P<currency>[A-Z]{3})\s*(?P<value>[\d,]+\.\d{2})",
        "total_amount": r"Total Amount:\s*(?P<currency>[A-Z]{3})\s*(?P<value>[\d,]+\.\d{2})",
    }

    def extract(self, path: Path) -> DocumentRecord:
        text = path.read_text(encoding="utf-8")
        record = DocumentRecord(source_file=path.name)
        matched_fields = 0
        total_fields = len(self.FIELD_PATTERNS) + len(self.AMOUNT_PATTERNS)

        for field_name, pattern in self.FIELD_PATTERNS.items():
            match = re.search(pattern, text)
            if match:
                setattr(record, field_name, match.group("value").strip())
                matched_fields += 1

        for field_name, pattern in self.AMOUNT_PATTERNS.items():
            match = re.search(pattern, text)
            if match:
                record.currency = match.group("currency")
                amount = float(match.group("value").replace(",", ""))
                setattr(record, field_name, amount)
                matched_fields += 1

        record.extraction_confidence = matched_fields / total_fields
        return record

