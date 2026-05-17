from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from document_pipeline.extractor import RegexInvoiceExtractor
from document_pipeline.pipeline import DocumentPipeline
from document_pipeline.validator import DocumentValidator


class DocumentPipelineTests(unittest.TestCase):
    def test_extractor_reads_core_fields(self) -> None:
        sample = PROJECT_ROOT / "data" / "samples" / "invoice_001.txt"
        record = RegexInvoiceExtractor().extract(sample)

        self.assertEqual(record.document_id, "INV-2026-001")
        self.assertEqual(record.supplier, "Rhein Components GmbH")
        self.assertEqual(record.purchase_order, "PO-77841")
        self.assertEqual(record.total_amount, 2189.60)
        self.assertGreaterEqual(record.extraction_confidence, 0.9)

    def test_validator_marks_problem_document_for_review(self) -> None:
        sample = PROJECT_ROOT / "data" / "samples" / "invoice_003_needs_review.txt"
        record = RegexInvoiceExtractor().extract(sample)
        validated = DocumentValidator().validate(record)

        self.assertEqual(validated.status, "needs_review")
        issue_messages = [issue.message for issue in validated.issues]
        self.assertIn("Missing required field: purchase_order", issue_messages)
        self.assertTrue(any("Due date is before" in msg for msg in issue_messages))
        self.assertTrue(any("Total amount should be" in msg for msg in issue_messages))

    def test_pipeline_creates_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_dir = temp_path / "samples"
            output_dir = temp_path / "outputs"
            shutil.copytree(PROJECT_ROOT / "data" / "samples", input_dir)

            summary = DocumentPipeline(input_dir, output_dir).run()

            self.assertEqual(summary.total_documents, 3)
            self.assertEqual(summary.approved_documents, 2)
            self.assertEqual(summary.exception_documents, 1)
            self.assertTrue((output_dir / "extracted_documents.csv").exists())
            self.assertTrue((output_dir / "exceptions.csv").exists())
            self.assertTrue((output_dir / "dashboard.html").exists())


if __name__ == "__main__":
    unittest.main()

