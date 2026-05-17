from __future__ import annotations

from datetime import date

from .models import DocumentRecord, ValidationIssue


class DocumentValidator:
    REQUIRED_FIELDS = [
        "document_id",
        "supplier",
        "invoice_date",
        "due_date",
        "purchase_order",
        "department",
        "cost_center",
    ]

    def validate(self, record: DocumentRecord) -> DocumentRecord:
        record.issues.clear()
        self._validate_required_fields(record)
        self._validate_dates(record)
        self._validate_amounts(record)
        self._validate_confidence(record)
        record.status = "approved" if not record.issues else "needs_review"
        return record

    def _validate_required_fields(self, record: DocumentRecord) -> None:
        for field_name in self.REQUIRED_FIELDS:
            if not getattr(record, field_name):
                record.issues.append(
                    ValidationIssue(
                        field=field_name,
                        message=f"Missing required field: {field_name}",
                    )
                )

    def _validate_dates(self, record: DocumentRecord) -> None:
        invoice_date = self._parse_date(record.invoice_date)
        due_date = self._parse_date(record.due_date)

        if record.invoice_date and invoice_date is None:
            record.issues.append(
                ValidationIssue("invoice_date", "Invoice date is not a valid date")
            )
        if record.due_date and due_date is None:
            record.issues.append(
                ValidationIssue("due_date", "Due date is not a valid date")
            )
        if invoice_date and due_date and due_date < invoice_date:
            record.issues.append(
                ValidationIssue("due_date", "Due date is before invoice date")
            )

    def _validate_amounts(self, record: DocumentRecord) -> None:
        if record.net_amount <= 0:
            record.issues.append(
                ValidationIssue("net_amount", "Net amount must be greater than zero")
            )
        if record.tax_amount < 0:
            record.issues.append(
                ValidationIssue("tax_amount", "Tax amount cannot be negative")
            )
        if record.total_amount <= 0:
            record.issues.append(
                ValidationIssue("total_amount", "Total amount must be greater than zero")
            )

        expected_total = round(record.net_amount + record.tax_amount, 2)
        if record.total_amount and abs(expected_total - record.total_amount) > 0.05:
            record.issues.append(
                ValidationIssue(
                    "total_amount",
                    f"Total amount should be {record.currency} {expected_total:,.2f}",
                )
            )

    def _validate_confidence(self, record: DocumentRecord) -> None:
        if record.extraction_confidence < 0.85:
            record.issues.append(
                ValidationIssue(
                    "extraction_confidence",
                    "Extraction confidence is below review threshold",
                    severity="warning",
                )
            )

    @staticmethod
    def _parse_date(value: str) -> date | None:
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None

