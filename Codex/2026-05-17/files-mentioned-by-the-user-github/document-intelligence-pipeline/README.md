# Document Intelligence Pipeline

Free local prototype of an enterprise document processing pipeline. It reads sample invoice-like business documents, extracts structured fields, validates the data, separates clean documents from exceptions, and generates an HTML operations dashboard.

This project is designed for a beginner to build and explain, while still showing enterprise thinking: document intake, extraction, validation, exception handling, structured outputs, reporting, and an upgrade path to Azure AI, Dataverse, Power BI, and Power Automate.

## What This Solves

Many enterprise teams still process operational documents manually: invoices, delivery notes, quality forms, purchase orders, and supplier documents. The manual process usually means opening a PDF, copying fields into Excel or ERP screens, checking totals, and sending exceptions by email.

This pipeline shows how that process can be automated end to end.

## Business Impact

| Metric | Manual Process | This Prototype |
|---|---:|---:|
| Processing time per document | 8-12 minutes | less than 5 seconds |
| Manual copy-paste steps | 8-15 fields | 0 fields |
| Exception visibility | Email or spreadsheet notes | Dedicated exception report |
| Reporting | Manual Excel update | Auto-generated dashboard |

The sample numbers are realistic estimates for interview storytelling. In a real company, these would be measured with actual process data before and after deployment.

## How It Works

```text
Sample documents (.txt)
        |
        v
Local extraction layer
        |
        v
Validation rules
        |
        +--> Approved records
        |
        +--> Exception report
        |
        v
CSV + JSON outputs + HTML dashboard
```

## Tech Stack

| Layer | Free Local Version | Enterprise Version |
|---|---|---|
| Document input | Sample text files | SharePoint, OneDrive, email inbox, SFTP |
| Extraction | Python regex parser | Azure AI Document Intelligence |
| Validation | Python business rules | Python service, Azure Functions, Logic Apps |
| Storage | CSV and JSON files | Dataverse, SQL Server, Azure Blob Storage |
| Dashboard | Static HTML report | Power BI semantic model and report |
| Alerts | Exception CSV | Power Automate or Teams notifications |

## Project Structure

```text
document-intelligence-pipeline/
|-- data/
|   `-- samples/              # Sample business documents
|-- docs/
|   |-- architecture.md        # Beginner and enterprise architecture
|   `-- interview_notes.md     # How to explain this project
|-- src/
|   `-- document_pipeline/
|       |-- extractor.py       # Field extraction logic
|       |-- validator.py       # Business validation rules
|       |-- storage.py         # CSV and JSON writers
|       |-- dashboard.py       # HTML dashboard renderer
|       `-- pipeline.py        # End-to-end orchestration
|-- tests/
|   `-- test_pipeline.py
|-- main.py
|-- requirements.txt
|-- .env.example
|-- .gitignore
`-- README.md
```

## Setup

Prerequisite: Python 3.10 or newer.

```bash
git clone https://github.com/YOUR-USERNAME/document-intelligence-pipeline
cd document-intelligence-pipeline
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

This project currently uses only the Python standard library, so the install step is intentionally simple.

## Usage

Run the complete pipeline:

```bash
python main.py
```

Run with custom folders:

```bash
python main.py --input-dir data/samples --output-dir outputs
```

Expected output files:

```text
outputs/
|-- dashboard.html
|-- extracted_documents.csv
|-- extracted_documents.json
`-- exceptions.csv
```

## Tests

```bash
python -m unittest discover tests
```

## Status

Working prototype:

- Extracts core invoice fields from sample documents
- Validates totals, dates, required fields, and confidence
- Produces structured CSV and JSON
- Creates an exception report
- Creates a simple business dashboard

## What I Would Add Next

1. Add PDF support with OCR.
2. Replace the local extractor with Azure AI Document Intelligence.
3. Store approved records in SQL Server or Dataverse.
4. Build a Power BI dashboard on top of the structured output.
5. Trigger the pipeline from SharePoint uploads using Power Automate.

## Interview Summary

I built a document intake pipeline that simulates how enterprises automate manual document processing. The free prototype runs locally with Python, but the architecture maps directly to Azure AI Document Intelligence, Dataverse or SQL, Power BI, and Power Automate. The project demonstrates business process thinking, not just coding.

