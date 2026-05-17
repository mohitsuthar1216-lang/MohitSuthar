from __future__ import annotations

from html import escape
from pathlib import Path

from .models import DocumentRecord


def render_dashboard(records: list[DocumentRecord], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    approved = [record for record in records if record.status == "approved"]
    exceptions = [record for record in records if record.status == "needs_review"]
    total_value = sum(record.total_amount for record in approved)
    currency = records[0].currency if records else "EUR"

    rows = "\n".join(_record_row(record) for record in records)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Document Intelligence Dashboard</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 32px;
      color: #1f2937;
      background: #f7f7f4;
    }}
    h1 {{ margin-bottom: 4px; }}
    .subtitle {{ color: #5f6b7a; margin-bottom: 24px; }}
    .kpis {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin-bottom: 24px;
    }}
    .kpi {{
      background: white;
      border: 1px solid #deded8;
      border-radius: 8px;
      padding: 16px;
    }}
    .kpi strong {{ display: block; font-size: 26px; margin-top: 6px; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: white;
      border: 1px solid #deded8;
    }}
    th, td {{
      padding: 10px;
      border-bottom: 1px solid #ededeb;
      text-align: left;
      font-size: 14px;
    }}
    th {{ background: #ecebe5; }}
    .approved {{ color: #0f766e; font-weight: 700; }}
    .needs_review {{ color: #b45309; font-weight: 700; }}
  </style>
</head>
<body>
  <h1>Document Intelligence Dashboard</h1>
  <div class="subtitle">Automated extraction, validation, and exception monitoring</div>

  <section class="kpis">
    <div class="kpi">Processed documents<strong>{len(records)}</strong></div>
    <div class="kpi">Approved<strong>{len(approved)}</strong></div>
    <div class="kpi">Needs review<strong>{len(exceptions)}</strong></div>
    <div class="kpi">Approved value<strong>{currency} {total_value:,.2f}</strong></div>
  </section>

  <table>
    <thead>
      <tr>
        <th>Document</th>
        <th>Supplier</th>
        <th>PO</th>
        <th>Total</th>
        <th>Status</th>
        <th>Issues</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
</body>
</html>
"""
    dashboard_path = output_dir / "dashboard.html"
    dashboard_path.write_text(html, encoding="utf-8")
    return dashboard_path


def _record_row(record: DocumentRecord) -> str:
    issue_text = "; ".join(issue.message for issue in record.issues) or "-"
    status_class = "approved" if record.status == "approved" else "needs_review"
    return f"""<tr>
  <td>{escape(record.document_id or record.source_file)}</td>
  <td>{escape(record.supplier)}</td>
  <td>{escape(record.purchase_order or "-")}</td>
  <td>{record.currency} {record.total_amount:,.2f}</td>
  <td class="{status_class}">{escape(record.status)}</td>
  <td>{escape(issue_text)}</td>
</tr>"""

