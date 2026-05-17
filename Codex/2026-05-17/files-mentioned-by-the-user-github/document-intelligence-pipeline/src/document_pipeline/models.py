from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationIssue:
    field: str
    message: str
    severity: str = "error"

    def to_dict(self) -> dict[str, str]:
        return {
            "field": self.field,
            "message": self.message,
            "severity": self.severity,
        }


@dataclass
class DocumentRecord:
    source_file: str
    document_id: str = ""
    supplier: str = ""
    invoice_date: str = ""
    due_date: str = ""
    purchase_order: str = ""
    department: str = ""
    cost_center: str = ""
    currency: str = "EUR"
    net_amount: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    extraction_confidence: float = 0.0
    status: str = "extracted"
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def issue_count(self) -> int:
        return len(self.issues)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_file": self.source_file,
            "document_id": self.document_id,
            "supplier": self.supplier,
            "invoice_date": self.invoice_date,
            "due_date": self.due_date,
            "purchase_order": self.purchase_order,
            "department": self.department,
            "cost_center": self.cost_center,
            "currency": self.currency,
            "net_amount": round(self.net_amount, 2),
            "tax_amount": round(self.tax_amount, 2),
            "total_amount": round(self.total_amount, 2),
            "extraction_confidence": round(self.extraction_confidence, 2),
            "status": self.status,
            "issue_count": self.issue_count,
            "issues": [issue.to_dict() for issue in self.issues],
        }

